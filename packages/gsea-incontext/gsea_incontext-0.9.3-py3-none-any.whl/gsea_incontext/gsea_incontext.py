#! python
# -*- coding: utf-8 -*-
from __future__ import division

import os, sys, logging, json
from collections import OrderedDict
from multiprocessing import Pool, cpu_count
import csv

import numpy as np
import pandas as pd
from numpy import log, exp

from gsea_incontext.algorithm import enrichment_score, enrichment_score_incontext, gsea_compute, ranking_metric
from gsea_incontext.algorithm import enrichment_score_tensor, gsea_compute_tensor
from gsea_incontext.parser import *
from gsea_incontext.plot import gsea_plot, heatmap
from gsea_incontext.utils import mkdirs, log_init, retry, DEFAULT_LIBRARY


class GSEAbase(object):
	"""Base class of GSEA"""

	def __init__(self):
		self.gene_sets='KEGG_2016'
		self.module='base'
		self.results=None
		self.res2d=None
		self.ranking=None
		self.ascending=False
		self.verbose=False
		self._processes=1
		self._logger=None


	def _set_cores(self):
		"""Set CPU numbers to be used."""

		cpu_num = cpu_count()-1
		if self._processes > cpu_num:
			cores = cpu_num
		elif self._processes < 1:
			cores = 1
		else:
			cores = self._processes
		# have to be int if user input is float
		self._processes = int(cores)

	def _load_ranking(self, rnk):
		"""Parse ranking file.

		The ranking file contains ranking correlation vector (or expression values) 
		and gene names or ids.

		:param rnk: the .rnk file of GSEA input or a pandas DataFrame, Series instance.
		:returns: a pandas Series with gene name indexed rankings
		"""

		# Load data
		if isinstance(rnk, pd.DataFrame):
			rank_metric = rnk.copy()
			# handle dataframe with gene_name as index.
			if rnk.shape[1] == 1: rank_metric = rnk.reset_index()
		elif isinstance(rnk, pd.Series):
			rank_metric = rnk.reset_index()
		elif os.path.isfile(rnk):
			rank_metric = pd.read_table(rnk, header=None, comment='#')
		else:
			raise Exception('Error parsing gene ranking values!')
		# sort ranking values from high to low
		rank_metric.sort_values(by=rank_metric.columns[1], ascending=self.ascending, inplace=True)
		# drop na values
		if rank_metric.isnull().any(axis=1).sum() >0:
			self._logger.warning("Input gene rankings contains NA values(gene name and ranking value), drop them all!")
			# print out NAs
			NAs = rank_metric[rank_metric.isnull().any(axis=1)]
			self._logger.debug('NAs list:\n'+NAs.to_string())
			rank_metric.dropna(how='any', inplace=True)
		# drop duplicate IDs, keep the first
		if rank_metric.duplicated(subset=rank_metric.columns[0]).sum() >0:
			self._logger.warning("Input gene rankings contains duplicated IDs, Only use the duplicated ID with highest value!")
			# print out duplicated IDs.
			dups = rank_metric[rank_metric.duplicated(subset=rank_metric.columns[0])]
			self._logger.debug('Dups list:\n'+dups.to_string())
			rank_metric.drop_duplicates(subset=rank_metric.columns[0], inplace=True, keep='first')
		# reset ranking index, because you have sort values and drop duplicates.
		rank_metric.reset_index(drop=True, inplace=True)
		rank_metric.columns = ['gene_name','rank']
		rankser = rank_metric.set_index('gene_name')['rank']
		self.ranking = rankser
		# return series
		return rankser

	def _load_background_ranking(self, rnks):
		"""Parse background ranking files.

		Load the gene ranking lists for all experiments to be used as the null background set during the
		permutation procedure.

		:param background_rnks: either a txt file containing paths to the .rnk files or a pandas DataFrame 
			with each column being a rank-ordered list of genes
		:returns: a list of lists, each element is a rank-ordered list of genes from an experiment
		"""

		bg_rnks = None

		if isinstance(rnks, pd.DataFrame):
			bg_rnks = rnks.transpose().values.tolist()
		elif os.path.isfile(rnks):
			f = pd.read_table(rnks, header=None, comment='#')
			if f.shape[1] == 1:
				compiled_rnks = []
				for r in f[0].values.tolist():
					if r.endswith(".rnk"):
						rnk = pd.read_table(r, header=None, comment='#')
						if rnk.shape[1] == 2:
							compiled_rnks.append(rnk[0].values.tolist())
				bg_rnks = compiled_rnks
			else:
				bg_rnks = f.transpose().values.tolist()
		elif os.path.isdir(rnks):
			compiled_rnks = []
			for f in os.listdir(rnks):
				if f.endswith(".rnk"):
					rnk = pd.read_table(os.path.join(rnks, f), header=None, comment='#')
					if rnk.shape[1] >= 2:
						compiled_rnks.append(rnk[0].values.tolist())
			bg_rnks = compiled_rnks
		else:
			raise Exception('Error parsing gene ranking values!')

		# remove NA values (v!=v only for NaN)
		for i in range(len(bg_rnks)):
			bg_rnks[i] = filter(lambda v: v==v, bg_rnks[i])

		# drop duplicate IDs, keep the first
		cleaned_rnks = [list(dict.fromkeys(lst)) for lst in bg_rnks]
		self._logger.debug('Background rank files used: %i' % len(cleaned_rnks))
		return cleaned_rnks

	def load_gmt(self, gene_list, gmt):
		"""Load gene set dict."""

		genesets_dict = self.parse_gmt(gmt)
		subsets = list(genesets_dict.keys())
		for subset in subsets:
			tag_indicator = np.in1d(gene_list, genesets_dict.get(subset), assume_unique=True)
			tag_len = tag_indicator.sum()
			if  self.min_size <= tag_len <= self.max_size: continue
			del genesets_dict[subset]

		filsets_num = len(subsets) - len(genesets_dict)
		self._logger.info("%04d gene_sets have been filtered out when max_size=%s and min_size=%s"%(filsets_num, self.max_size, self.min_size))

		if filsets_num == len(subsets):
			self._logger.error("No gene sets passed throught filtering condition!!!, try new paramters again!\n" +\
							   "Note: check gene name, gmt file format, or filtering size." )
			sys.exit(0)

		self._gmtdct=genesets_dict
		return genesets_dict

	def parse_gmt(self, gmt):
		"""Parse .gmt file into a dict."""

		if gmt.lower().endswith(".gmt"):
			self._logger.info("User Defined gene sets is given.......continue..........")
			with open(gmt) as genesets:
				 genesets_dict = { line.strip().split("\t")[0]: line.strip().split("\t")[2:]
								  for line in genesets.readlines()}
			return genesets_dict

		elif gmt in DEFAULT_LIBRARY:
			pass
		elif gmt in self.get_libraries():
			pass
		else:
			self._logger.error("No supported gene_sets: %s"%gmt)
			sys.exit(0)

		self._logger.info("Downloading and generating Enrichr library gene sets......")
		tmpname = "enrichr." + gmt + ".gmt"
		tempath = os.path.join(self.outdir, tmpname)
		# if file already downloaded
		if os.path.isfile(tempath):
			self._logger.info("Enrichr library gene sets already downloaded, use local file")
			return self.parse_gmt(tempath)
		else:
			return self._download_libraries(gmt)

	def get_libraries(self):
		"""Return active enrichr library name from offical API"""

		lib_url='http://amp.pharm.mssm.edu/Enrichr/datasetStatistics'
		libs_json = json.loads(requests.get(lib_url).text)
		libs = [lib['libraryName'] for lib in libs_json['statistics']]
		return sorted(libs)

	def _download_libraries(self, libname):
		"""Download enrichr libraries"""

		s = retry(5)
		# query string
		ENRICHR_URL = 'http://amp.pharm.mssm.edu/Enrichr/geneSetLibrary'
		query_string = '?mode=text&libraryName=%s'
		# get
		response = s.get( ENRICHR_URL + query_string % libname, timeout=None)
		if not response.ok:
			raise Exception('Error fetching enrichment results, check internet connection first.')
		# reformat to dict and wirte to disk
		genesets_dict = {}
		outname = "enrichr.%s.gmt"%libname
		gmtout = open(os.path.join(self.outdir, outname),"w")
		for line in response.iter_lines(chunk_size=1024, decode_unicode='utf-8'):
			line=line.strip()
			k = line.split("\t")[0]
			v = list(map(lambda x: x.split(",")[0], line.split("\t")[2:]))
			genesets_dict.update({ k: v})
			outline = "%s\t\t%s\n"%(k, "\t".join(v))
			gmtout.write(outline)
		gmtout.close()
		return genesets_dict

	def _plotting(self, rank_metric, results, res2d,
				 graph_num, outdir, format, figsize, module=None, data=None,
				 classes=None, phenoPos='', phenoNeg=''):
		"""Plotting API

		:param rank_metric: sorted pd.Series with rankings values.
		:param results: self.results
		:param data: preprocessed expression table
		"""

		# plotting
		top_term = res2d.head(graph_num).index

		# multi-threading
		pool = Pool(processes=self._processes)

		for gs in top_term:
			hit = results.get(gs)['hits_indices']
			NES = 'nes' if module != 'ssgsea' else 'es'
			# gsea_plot(rank_metric=rank_metric, enrich_term=gs, hit_ind=hit,
			#           nes=results.get(gs)[NES], pval=results.get(gs)['pval'], fdr=results.get(gs)['fdr'],
			#           RES=results.get(gs)['RES'], phenoPos=phenoPos, phenoNeg=phenoNeg, figsize=figsize,
			#           format=self.format, outdir=self.outdir, module=self.module)
			pool.apply_async(gsea_plot, args=(rank_metric, gs, hit, results.get(gs)[NES],
											  results.get(gs)['pval'],results.get(gs)['fdr'],
											  results.get(gs)['RES'],
											  phenoPos, phenoNeg, figsize, self.format,
											  self.outdir,self.module))
		pool.close()
		pool.join()

		if module == 'gsea':
			width = len(classes) if len(classes) >= 6 else  5
			cls_booA =list(map(lambda x: True if x == phenoPos else False, classes))
			cls_booB =list(map(lambda x: True if x == phenoNeg else False, classes))
			datA = data.loc[:, cls_booA]
			datB = data.loc[:, cls_booB]
			datAB=pd.concat([datA,datB], axis=1)
			pool_heat = Pool(self._processes)

			# no values need to be returned
			for gs in top_term:
				hit = results.get(gs)['hits_indices']
				pool_heat.apply_async(heatmap, args=(datAB.iloc[hit], gs, outdir, 0,
													(width, len(hit)/2), format))
				# heatmap(datAB.iloc[hit], gs, outdir, 0, (width, len(hit)/2), format)
			pool_heat.close()
			pool_heat.join()

	def _save_results(self, zipdata, outdir, module, gmt, rank_metric, permutation_type):
		"""Reformat gsea results and save to txt."""

		res = OrderedDict()
		for gs,gseale,ind,RES in zipdata:
			rdict = OrderedDict()
			rdict['es'] = gseale[0]
			rdict['nes'] = gseale[1]
			rdict['pval'] = gseale[2]
			rdict['fdr'] = gseale[3]
			rdict['geneset_size'] = len(gmt[gs])
			rdict['matched_size'] = len(ind)
			#reformat gene list.
			_genes = rank_metric.index.values[ind]
			rdict['genes'] = ",".join([ g.strip() for g in _genes ])

			rdict['RES'] = RES
			rdict['hits_indices'] = ind
			res[gs] = rdict

		res_df = pd.DataFrame.from_dict(res, orient='index')
		res_df.index.name = 'Term'
		res_df.sort_values(by='fdr', inplace=True)
		res_df.drop(['RES','hits_indices'], axis=1, inplace=True)

		out = os.path.join(outdir,'gsea_incontext.{b}.{c}.report.csv'.format(b=module, c=permutation_type))
		if self.module == 'ssgsea':
			out = out.replace(".csv",".txt")
			with open(out, 'a') as f:
				f.write('# normalize enrichment scores by random permutation procedure (GSEA method)\n')
				f.write("# might not proper for publication\n")
				res_df.to_csv(f, sep='\t')
		else:
			res_df.to_csv(out)

		self.res2d = res_df
		self.results  = res
		return


class GSEA(GSEAbase):
	"""GSEA main tool"""

	def __init__(self, data, gene_sets, classes, outdir='GSEA_ouput',
				 min_size=15, max_size=500, permutation_num=1000,
				 weighted_score_type=1, permutation_type='gene_set',
				 method='log2_ratio_of_classes', ascending=False,
				 processes=1, figsize=(6.5,6), format='pdf', graph_num=20,
				 no_plot=False, seed=None, verbose=False):

		self.data = data
		self.gene_sets=gene_sets
		self.classes=classes
		self.outdir=outdir
		self.permutation_type=permutation_type
		self.method=method
		self.min_size=min_size
		self.max_size=max_size
		self.permutation_num=int(permutation_num) if int(permutation_num) > 0 else 0
		self.weighted_score_type=weighted_score_type
		self.ascending=ascending
		self._processes=processes
		self.figsize=figsize
		self.format=format
		self.graph_num=int(graph_num)
		self.seed=seed
		self.verbose=bool(verbose)
		self.module='gsea'
		self.ranking=None
		self._noplot=no_plot
		# init logger
		mkdirs(self.outdir)
		_gset =os.path.split(self.gene_sets)[-1].lower().rstrip(".gmt")
		outlog = os.path.join(self.outdir,"gsea_incontext.%s.%s.log"%(self.module, _gset))
		self._logger = log_init(outlog=outlog,
								log_level=logging.INFO if self.verbose else logging.WARNING)

	def load_data(self, cls_vec):
		"""Pre-process file or DataFrame."""

		if isinstance(self.data, pd.DataFrame) :
			exprs = self.data.copy()
			# handle index is gene_names
			if exprs.index.dtype == 'O':
				exprs = exprs.reset_index()
		elif os.path.isfile(self.data) :
			# GCT input format?
			if self.data.endswith("gct"):
				exprs = pd.read_table(self.data, skiprows=1, comment='#')
			else:
				exprs = pd.read_table(self.data, comment='#')
		else:
			raise Exception('Error parsing gene expression dataframe!')
			sys.exit(1)

		# drop duplicated gene names
		if exprs.iloc[:,0].duplicated().sum() > 0:
			self._logger.warning("Warning: dropping duplicated gene names, only keep the first values")
			exprs.drop_duplicates(subset=exprs.columns[0], inplace=True) #drop duplicate gene_names.
		if exprs.isnull().any().sum() > 0:
			self._logger.warning("Warning: Input data contains NA, filled NA with 0")
			exprs.dropna(how='all', inplace=True) #drop rows with all NAs
			exprs = exprs.fillna(0)
		# set gene name as index
		exprs.set_index(keys=exprs.columns[0], inplace=True)
		# select numberic columns
		df = exprs.select_dtypes(include=[np.number])
		# drop any genes which std ==0
		df_std =  df.groupby(by=cls_vec, axis=1).std()
		df =  df[~df_std.isin([0]).any(axis=1)]
		df = df + 0.00001 # we don't like zeros!!!
		return df

	def run(self):
		"""Run GSEA main procedure."""

		assert self.permutation_type in ["phenotype", "gene_set"]
		assert self.min_size <= self.max_size

		# start analysis
		self._logger.info("Parsing data files for GSEA.............................")
		# phenotype labels parsing
		phenoPos, phenoNeg, cls_vector = gsea_cls_parser(self.classes)
		# select correct expression genes and values.
		dat = self.load_data(cls_vector)
		# data frame must have lenght > 1
		assert len(dat) > 1
		# ranking metrics calculation.
		dat2 = ranking_metric(df=dat, method=self.method, pos=phenoPos, neg=phenoNeg,
							  classes=cls_vector, ascending=self.ascending)
		# filtering out gene sets and build gene sets dictionary
		gmt = self.load_gmt(gene_list=dat2.index.values, gmt=self.gene_sets)

		self._logger.info("%04d gene_sets used for further statistical testing....."% len(gmt))
		self._logger.info("Start to run GSEA...Might take a while..................")
		# cpu numbers
		self._set_cores()
		# compute ES, NES, pval, FDR, RES
		dataset = dat if self.permutation_type =='phenotype' else dat2
		gsea_results,hit_ind,rank_ES, subsets = gsea_compute_tensor(data=dataset, gmt=gmt, n=self.permutation_num,
															 weighted_score_type=self.weighted_score_type,
															 permutation_type=self.permutation_type,
															 method=self.method,
															 pheno_pos=phenoPos, pheno_neg=phenoNeg,
															 classes=cls_vector, ascending=self.ascending,
															 processes=self._processes, seed=self.seed)
		
		self._logger.info("Start to generate gsea_incontext reports, and produce figures...")
		res_zip = zip(subsets, list(gsea_results), hit_ind, rank_ES)
		self._save_results(zipdata=res_zip, outdir=self.outdir, module=self.module,
								   gmt=gmt, rank_metric=dat2, permutation_type=self.permutation_type)

		# Plotting
		if not self._noplot:
			heat_dat = dat.loc[dat2.index]
			self._plotting(rank_metric=dat2, results=self.results, res2d=self.res2d,
						   graph_num=self.graph_num, outdir=self.outdir,
						   figsize=self.figsize, format=self.format, module=self.module,
						   data=heat_dat, classes=cls_vector, phenoPos=phenoPos, phenoNeg=phenoNeg)

		self._logger.info("Congratulations. GSEApy run successfully................\n")
		return


class Prerank(GSEAbase):
	"""GSEAPreranked tool"""

	def __init__(self, rnk, gene_sets, outdir='GSEA_prerank',
				 pheno_pos='Pos', pheno_neg='Neg', min_size=15, max_size=500,
				 permutation_num=1000, weighted_score_type=1,
				 ascending=False, processes=1, figsize=(6.5,6), format='pdf',
				 graph_num=20, no_plot=False, seed=None, verbose=False):

		self.rnk =rnk
		self.gene_sets=gene_sets
		self.outdir=outdir
		self.pheno_pos=pheno_pos
		self.pheno_neg=pheno_neg
		self.min_size=min_size
		self.max_size=max_size
		self.permutation_num=int(permutation_num) if int(permutation_num) > 0 else 0
		self.weighted_score_type=weighted_score_type
		self.ascending=ascending
		self.figsize=figsize
		self.format=format
		self.graph_num=int(graph_num)
		self.seed=seed
		self.verbose=bool(verbose)
		self.ranking=None
		self.module='prerank'
		self._processes=processes
		self._noplot=no_plot
		# init logger
		mkdirs(self.outdir)
		_gset =os.path.split(self.gene_sets)[-1].lower().rstrip(".gmt")
		outlog = os.path.join(self.outdir,"gsea_incontext.%s.%s.log"%(self.module, _gset))
		self._logger = log_init(outlog=outlog,
								log_level=logging.INFO if self.verbose else logging.WARNING)

	def run(self):
		"""Run GSEAPreranked workflow."""

		assert self.min_size <= self.max_size

		# parsing rankings
		dat2 = self._load_ranking(self.rnk)
		assert len(dat2) > 1

		# cpu numbers
		self._set_cores()
		# Start Analysis
		self._logger.info("Parsing data files for GSEA.............................")
		# filtering out gene sets and build gene sets dictionary
		gmt = self.load_gmt(gene_list=dat2.index.values, gmt=self.gene_sets)

		self._logger.info("%04d gene_sets used for further statistical testing....."% len(gmt))
		self._logger.info("Start to run GSEA...Might take a while..................")
		# compute ES, NES, pval, FDR, RES
		gsea_results, hit_ind,rank_ES, subsets = gsea_compute(data=dat2, n=self.permutation_num, gmt=gmt,
															  weighted_score_type=self.weighted_score_type,
															  permutation_type='gene_set', method=None,
															  pheno_pos=self.pheno_pos, pheno_neg=self.pheno_neg,
															  classes=None, ascending=self.ascending,
															  processes=self._processes, seed=self.seed)
		self._logger.info("Start to generate gsea_incontext reports, and produce figures...")
		res_zip = zip(subsets, list(gsea_results), hit_ind, rank_ES)
		self._save_results(zipdata=res_zip, outdir=self.outdir, module=self.module,
								   gmt=gmt, rank_metric=dat2, permutation_type="gene_sets")

		# Plotting
		if not self._noplot:
			self._plotting(rank_metric=dat2, results=self.results, res2d=self.res2d,
						   graph_num=self.graph_num, outdir=self.outdir,
						   figsize=self.figsize, format=self.format,
						   module=self.module, phenoPos=self.pheno_pos, phenoNeg=self.pheno_neg)

		self._logger.info("Congratulations. GSEApy run successfully................\n")

		return


class GSEA_InContext(GSEAbase):
	"""GSEA-InContext algorithm: GSEAPreranked using background experiments as the null"""

	def __init__(self, rnk, gene_sets, background_rnks, outdir='GSEA_InContext',
				 pheno_pos='Pos', pheno_neg='Neg', min_size=15, max_size=500,
				 permutation_num=1000, weighted_score_type=1,
				 ascending=False, processes=1, figsize=(6.5,6), format='pdf',
				 graph_num=20, no_plot=False, seed=None, verbose=False):

		self.rnk =rnk
		self.gene_sets=gene_sets
		self.background_rnks=background_rnks
		self.outdir=outdir
		self.pheno_pos=pheno_pos
		self.pheno_neg=pheno_neg
		self.min_size=min_size
		self.max_size=max_size
		self.permutation_num=int(permutation_num) if int(permutation_num) > 0 else 0
		self.weighted_score_type=weighted_score_type
		self.ascending=ascending
		self.figsize=figsize
		self.format=format
		self.graph_num=int(graph_num)
		self.seed=seed
		self.verbose=bool(verbose)
		self.ranking=None
		self.module='incontext'
		self._processes=processes
		self._noplot=no_plot
		# init logger
		mkdirs(self.outdir)
		_gset =os.path.split(self.gene_sets)[-1].lower().rstrip(".gmt")
		outlog = os.path.join(self.outdir,"gsea_incontext.%s.%s.log"%(self.module, _gset))
		self._logger = log_init(outlog=outlog,
								log_level=logging.INFO if self.verbose else logging.WARNING)

	def run(self):
		"""Run GSEA-PEN workflow."""

		assert self.min_size <= self.max_size

		# parse rankings
		dat2 = self._load_ranking(self.rnk)
		assert len(dat2) > 1

		# parse background gene lists
		if self.background_rnks.endswith('.csv'):
			with open(self.background_rnks, "r") as f:
				reader = csv.reader(f)
				bg_lists = list(reader)
			print(len(bg_lists))
		else:
			bg_lists = self._load_background_ranking(self.background_rnks)
		assert len(bg_lists) > 3

		# cpu numbers
		self._set_cores()
		# Start Analysis
		self._logger.info("Parsing data files for GSEA-InContext")
		# filtering out gene sets and build gene sets dictionary
		gmt = self.load_gmt(gene_list=dat2.index.values, gmt=self.gene_sets)

		self._logger.info("%04d gene_sets used for further statistical testing" % len(gmt))
		self._logger.info("Running GSEA-InContext")

		# compute ES, NES, pval, FDR, RES
		gsea_results, hit_ind,rank_ES, subsets = gsea_compute(data=dat2, n=self.permutation_num, gmt=gmt,
			weighted_score_type=self.weighted_score_type, method=None, pheno_pos=self.pheno_pos, 
			pheno_neg=self.pheno_neg, classes=None, ascending=self.ascending, processes=self._processes, 
			seed=self.seed, bg_lists=bg_lists, permutation_type='incontext')  
			# bg_lists, permutation_type determine whether GSEA-InContext algorithm is used

		self._logger.info("Generating GSEA-InContext reports figures in %s" % self.outdir)
		res_zip = zip(subsets, list(gsea_results), hit_ind, rank_ES)
		self._save_results(zipdata=res_zip, outdir=self.outdir, module=self.module,
								   gmt=gmt, rank_metric=dat2, permutation_type="gene_sets")

		# Plotting
		if not self._noplot:
			self._plotting(rank_metric=dat2, results=self.results, res2d=self.res2d,
						   graph_num=self.graph_num, outdir=self.outdir,
						   figsize=self.figsize, format=self.format,
						   module=self.module, phenoPos=self.pheno_pos, phenoNeg=self.pheno_neg)

		self._logger.info("Done! GSEA-InContext run successfully.\n")

		return


class SingleSampleGSEA(GSEAbase):
	"""GSEA extension: single sample GSEA"""

	def __init__(self, data, gene_sets, outdir="GSEA_SingleSample", sample_norm_method='rank',
				 min_size=15, max_size=2000, permutation_num=0, weighted_score_type=0.25,
				 scale=True, ascending=False, processes=1, figsize=(7,6), format='pdf',
				 graph_num=20, no_plot=False, seed=None, verbose=False):
		self.data=data
		self.gene_sets=gene_sets
		self.outdir=outdir
		self.sample_norm_method=sample_norm_method
		self.weighted_score_type=weighted_score_type
		self.scale = scale
		self.min_size=min_size
		self.max_size=max_size
		self.permutation_num=int(permutation_num) if int(permutation_num) > 0 else 0
		self.ascending=ascending
		self.figsize=figsize
		self.format=format
		self.graph_num=int(graph_num)
		self.seed=seed
		self.verbose=bool(verbose)
		self.ranking=None
		self.module='ssgsea'
		self._processes=processes
		self._noplot=no_plot
		# init logger
		mkdirs(self.outdir)
		_gset =os.path.split(self.gene_sets)[-1].lower().rstrip(".gmt")
		outlog = os.path.join(self.outdir,"gsea_incontext.%s.%s.log"%(self.module, _gset))
		self._logger = log_init(outlog=outlog,
								log_level=logging.INFO if self.verbose else logging.WARNING)

	def corplot(self):
		"""Make NES Correlation plot."""
	def setplot(self):
		"""Set ranked genes' location plot."""

	def load_data(self):
		"""Load data for ssGSEA."""

		exprs = self.data
		if isinstance(exprs, pd.DataFrame):
			rank_metric = exprs.copy()
			# handle dataframe with gene_name as index.
			self._logger.debug("Input data is a DataFrame with gene names")
			# handle index is not gene_names
			if rank_metric.index.dtype != 'O':
				rank_metric.set_index(keys=rank_metric.columns[0], inplace=True)

			rank_metric = rank_metric.select_dtypes(include=[np.number])
		elif isinstance(exprs, pd.Series):
			# change to DataFrame
			self._logger.debug("Input data is a Series with gene names")
			rank_metric = pd.DataFrame(exprs)
			# rename col if name attr is none
			rank_metric.columns = ["sample1"]
		elif os.path.isfile(exprs):
			# GCT input format?
			if exprs.endswith("gct"):
				rank_metric = pd.read_table(exprs, skiprows=1, comment='#', index_col=0)
			else:
				# just txt file like input
				rank_metric = pd.read_table(exprs, comment='#', index_col=0)
				if rank_metric.shape[1] ==1:
					# rnk file like input
					rank_metric = pd.read_table(exprs, header=None, comment='#',
												names=['sample1'], index_col=0)
			# select numbers
			rank_metric = rank_metric.select_dtypes(include=[np.number])
		else:
			raise Exception('Error parsing gene ranking values!')

		if rank_metric.index.duplicated().sum() > 0:
			self._logger.warning("Warning: dropping duplicated gene names, only keep the first values")
			rank_metric = rank_metric.loc[rank_metric.index.drop_duplicates(keep='first')]
			rank_metric = rank_metric.loc[rank_metric.index.dropna()]
		if rank_metric.isnull().any().sum() > 0:
			self._logger.warning("Warning: Input data contains NA, filled NA with 0")
			rank_metric = rank_metric.fillna(0)

		return rank_metric

	def norm_samples(self, dat):
		"""Normalize samples.
		See here: http://rowley.mit.edu/caw_web/ssGSEAProjection/ssGSEAProjection.Library.R
		"""

		if self.sample_norm_method == 'rank':
			data = dat.rank(axis=0, method='average', na_option='bottom')
			data = 10000*data / data.shape[0]
		elif self.sample_norm_method == 'log_rank':
			data = dat.rank(axis=0, method='average', na_option='bottom')
			data = log(10000*data / data.shape[0] + exp(1))
		elif self.sample_norm_method == 'log':
			dat[dat < 1] = 1
			data = log(dat + exp(1))
		elif self.sample_norm_method == 'custom':
			self._logger.info("Use custom rank metric for ssGSEA")
		else:
			sys.stderr.write("No supported method: %s"%self.sample_norm_method)
			sys.exit(0)

		return data

	def run(self):
		"""Run entry."""

		self._logger.info("Parsing data files for ssGSEA...........................")
		# load data
		data = self.load_data()
		# normalized samples, and rank
		normdat = self.norm_samples(data)
		# filtering out gene sets and build gene sets dictionary
		gmt = self.load_gmt(gene_list=normdat.index.values, gmt=self.gene_sets)
		self._logger.info("%04d gene_sets used for further statistical testing....."% len(gmt))
		# set cpu numbers
		self._set_cores()
		# start analsis
		self._logger.info("Start to run ssGSEA...Might take a while................")
		if self.permutation_num == 0 :
			# ssGSEA without permutation
			self.runSamples(df=normdat, gmt=gmt)
		else:
			# run permutation procedure and calculate pvals, fdrs
			self._logger.info("run ssGSEA with permutation procedure, might take a while")
			self.runSamplesPermu(df=normdat, gmt=gmt)

	def runSamplesPermu(self, df, gmt=None):
		"""Run Single Sample GSEA workflow with permutation procedure."""

		assert self.min_size <= self.max_size
		mkdirs(self.outdir)
		self.resultsOnSamples = OrderedDict()
		outdir = self.outdir
		# iter throught each sample
		for name, ser in df.iteritems():
			self.outdir = os.path.join(outdir, str(name))
			self._logger.info("Run Sample: %s " % name)
			mkdirs(self.outdir)
			# sort ranking values from high to low or reverse
			dat2 = ser.sort_values(ascending=self.ascending)
			# reset integer index, or caused unwanted problems
			# df.reset_index(drop=True, inplace=True)

			# compute ES, NES, pval, FDR, RES
			gsea_results, hit_ind,rank_ES, subsets = gsea_compute(data=dat2, n=self.permutation_num, gmt=gmt,
																  weighted_score_type=self.weighted_score_type,
																  permutation_type='gene_set', method=None,
																  pheno_pos='', pheno_neg='',
																  classes=None, ascending=self.ascending,
																  processes=self._processes,
																  seed=self.seed, single=True, scale=self.scale)

			# write file
			res_zip = zip(subsets, list(gsea_results), hit_ind, rank_ES)
			self._save_results(zipdata=res_zip, outdir=self.outdir, module=self.module,
									   gmt=gmt, rank_metric=dat2, permutation_type="gene_sets")
			self.resultsOnSamples[name] = self.res2d.es
			# plotting
			if self._noplot: continue
			self._logger.info("Plotting Sample: %s \n" % name)
			self._plotting(rank_metric=dat2, results=self.results, res2d=self.res2d,
						   graph_num=self.graph_num, outdir=self.outdir,
						   figsize=self.figsize, format=self.format, module=self.module)

		# save es, nes to file
		self._save(outdir)

		return

	def runSamples(self, df, gmt=None):
		"""Run Single Sample GSEA workflow.
		Multiprocessing utility on samples.
		"""

		# df.index.values are gene_names
		# Save each sample results to odict
		self.resultsOnSamples = OrderedDict()
		outdir = self.outdir
		# run ssgsea for gct expression matrix
		#multi-threading
		subsets = sorted(gmt.keys())
		tempes=[]
		names=[]
		rankings=[]
		pool = Pool(processes=self._processes)
		for name, ser in df.iteritems():
			#prepare input
			dat = ser.sort_values(ascending=self.ascending)
			rankings.append(dat)
			names.append(name)
			genes_sorted, cor_vec = dat.index.values, dat.values
			rs = np.random.RandomState(self.seed)
			# apply_async
			tempes.append(pool.apply_async(enrichment_score_tensor,
										   args=(genes_sorted, cor_vec, gmt,
											   self.weighted_score_type,
											   self.permutation_num, rs, True,
											   self.scale)))
		pool.close()
		pool.join()
		# save results and plotting
		for i, temp in enumerate(tempes):
			name, rnk = names[i], rankings[i]
			self._logger.info("Calculate Enrichment Score for Sample: %s "%name)
			es, esnull, hit_ind, RES = temp.get()
			# create results subdir
			self.outdir= os.path.join(outdir, str(name))
			mkdirs(self.outdir)
			# save results
			self.resultsOnSamples[name] = pd.Series(data=es, index=subsets, name=name)
		# plotting
		#if self._noplot: continue
		self._logger.info("Plotting Sample: %s \n" % name)
		for i, term in enumerate(subsets):
			gsea_plot(rnk,term, hit_ind[i], es[i], 1, 1, RES[i],
				'', '', self.figsize, self.format, self.outdir, module=self.module)
		# save es, nes to file
		self._save(outdir)

		return

	def _save(self, outdir):
		"""Save ES and stats."""

		# save raw ES to one csv file
		samplesRawES = pd.DataFrame(self.resultsOnSamples)
		samplesRawES.index.name = 'Term|ES'
		# write es
		outESfile = os.path.join(outdir, "gsea_incontext.samples.raw.es.txt")
		with open(outESfile, 'a') as f:
			if self.scale:
				f.write('# scale the enrichment scores by number of genes in the gene sets\n')
				f.write('# this normalization has not effects on the final NES, ' + \
						'as indicated by Barbie et al., 2009, online methods, pg. 2\n')
			else:
				f.write('# raw enrichment scores of all data\n')
				f.write('# no scale es by numbers of genes in the gene sets\n')
			samplesRawES.to_csv(f, sep='\t')
		# normalize enrichment scores by using the entire data set, as indicated
		# by Barbie et al., 2009, online methods, pg. 2
		samplesNES = samplesRawES / (samplesRawES.values.max() - samplesRawES.values.min())
		samplesNES = samplesNES.copy()
		samplesNES.index.rename('Term|NES', inplace=True)
		outNESfile = os.path.join(outdir, "gsea_incontext.samples.normalized.es.txt")
		with open(outNESfile, 'a') as f:
			f.write('# normalize enrichment scores by using the entire data set\n')
			f.write('# as indicated by Barbie et al., 2009, online methods, pg. 2\n')
			samplesNES.to_csv(f, sep='\t')
		self.res2d = samplesNES
		self._logger.info("Congratulations. GSEApy run successfully................\n")

		return


class Replot(GSEAbase):
	"""Reproduce GSEA desktop output results."""

	def __init__(self, indir, outdir='GSEApy_Replot', weighted_score_type=1,
				  min_size=3, max_size=1000, figsize=(6.5,6), graph_num=20, format='pdf', verbose=False):
		self.indir=indir
		self.outdir=outdir
		self.weighted_score_type=weighted_score_type
		self.min_size=min_size
		self.max_size=max_size
		self.figsize=figsize
		self.fignum=int(graph_num)
		self.format=format
		self.verbose=bool(verbose)
		self.module='replot'
		self.gene_sets=None
		self.ascending=False
		# init logger
		mkdirs(self.outdir)
		outlog = os.path.join(self.outdir,"gsea_incontext.%s.%s.log"%(self.module,"run"))
		self._logger = log_init(outlog=outlog,
								log_level=logging.INFO if self.verbose else logging.WARNING)
	def run(self):
		"""Run Replot."""
		assert self.min_size <= self.max_size
		assert self.fignum > 0
		import glob
		from bs4 import BeautifulSoup

		# parsing files.......
		try:
			results_path = glob.glob(self.indir+'*/edb/results.edb')[0]
			rank_path =  glob.glob(self.indir+'*/edb/*.rnk')[0]
			gene_set_path =  glob.glob(self.indir+'*/edb/gene_sets.gmt')[0]
		except IndexError as e:
			sys.stderr.write("Could not locate GSEA files in the given directory!")
			sys.exit(1)
		# extract sample names from .cls file
		cls_path = glob.glob(self.indir+'*/edb/*.cls')
		if cls_path:
			phenoPos, phenoNeg, classes = gsea_cls_parser(cls_path[0])
		else:
			# logic for prerank results
			phenoPos, phenoNeg = '',''
		# start reploting
		self.gene_sets=gene_set_path
		# obtain gene sets
		gene_set_dict = self.parse_gmt(gmt=gene_set_path)
		# obtain rank_metrics
		rank_metric = self._load_ranking(rank_path)
		correl_vector =  rank_metric.values
		gene_list = rank_metric.index.values
		# extract each enriment term in the results.edb files and plot.
		database = BeautifulSoup(open(results_path), features='xml')
		length = len(database.findAll('DTG'))
		fig_num = self.fignum if self.fignum <= length else length
		for idx in range(fig_num):
			# extract statistical resutls from results.edb file
			enrich_term, hit_ind, nes, pval, fdr= gsea_edb_parser(results_path, index=idx)
			gene_set = gene_set_dict.get(enrich_term)
			# calculate enrichment score
			RES = enrichment_score(gene_list=gene_list, 
								   correl_vector=correl_vector,
								   gene_set=gene_set, 
								   weighted_score_type=self.weighted_score_type,
								   nperm=0)[-1]
			# plotting
			gsea_plot(rank_metric, enrich_term, hit_ind, nes, pval,
							fdr, RES, phenoPos, phenoNeg, self.figsize,
							self.format, self.outdir, self.module)

		self._logger.info("Congratulations! Your plots have been reproduced successfully!\n")


def gsea(data, gene_sets, cls, outdir='GSEA_', min_size=15, max_size=500, permutation_num=1000,
		  weighted_score_type=1,permutation_type='gene_set', method='log2_ratio_of_classes',
		  ascending=False, processes=1, figsize=(6.5,6), format='pdf',
		  graph_num=20, no_plot=False, seed=None, verbose=False):
	""" Run Gene Set Enrichment Analysis.

	:param data: Gene expression data table, pandas DataFrame, gct file.
	:param gene_sets: Enrichr Library name or .gmt gene sets file. Same input with GSEA.
	:param cls: a list or a .cls file format required for GSEA.
	:param str outdir: Results output directory.
	:param int permutation_num: Number of permutations for significance computation. Default: 1000.
	:param str permutation_type: Permutation type, "phenotype" for phenotypes, "gene_set" for genes.
	:param int min_size: Minimum allowed number of genes from gene set also the data set. Default: 15.
	:param int max_size: Maximum allowed number of genes from gene set also the data set. Default: 500.
	:param float weighted_score_type: Refer to :func:`algorithm.enrichment_score`. Default:1.
	:param method:  The method used to calculate a correlation or ranking. Default: 'log2_ratio_of_classes'.
		Others methods are:

			1. 'signal_to_noise'

				You must have at least three samples for each phenotype to use this metric.
				The larger the signal-to-noise ratio, the larger the differences of the means (scaled by the standard deviations);
				that is, the more distinct the gene expression is in each phenotype and the more the gene acts as a “class marker.”

			2. 't_test'

				Uses the difference of means scaled by the standard deviation and number of samples.
				Note: You must have at least three samples for each phenotype to use this metric.
				The larger the tTest ratio, the more distinct the gene expression is in each phenotype
				and the more the gene acts as a “class marker.”

			3. 'ratio_of_classes' (also referred to as fold change).

				Uses the ratio of class means to calculate fold change for natural scale data.

			4. 'diff_of_classes'
				
				Uses the difference of class means to calculate fold change for nature scale data

			5. 'log2_ratio_of_classes'

				Uses the log2 ratio of class means to calculate fold change for natural scale data.
				This is the recommended statistic for calculating fold change for log scale data.

	:param bool ascending: Sorting order of rankings. Default: False.
	:param int processes: Number of Processes you are going to use. Default: 1.
	:param list figsize: Matplotlib figsize, accept a tuple or list, e.g. [width,height]. Default: [6.5,6].
	:param str format: Matplotlib figure format. Default: 'pdf'.
	:param int graph_num: Plot graphs for top sets of each phenotype.
	:param bool no_plot: if equal to True, no figure will be draw. Default: False.
	:param seed: Random seed. expect an integer. Default:None.
	:param bool verbose: Bool, increase output verbosity, print out progress of your job, Default: False.

	:returns: Return a GSEA obj. All results stored to a dictionary, obj.results,
		where contains::

			| {es: enrichment score,
			| nes: normalized enrichment score,
			| p: P-value,
			| fdr: FDR,
			| size: gene set size,
			| matched_size: genes matched to the data,
			| genes: gene names from the data set}

	"""
	gs = GSEA(data, gene_sets, cls, outdir, min_size, max_size, permutation_num,
			  weighted_score_type, permutation_type, method, ascending, processes,
			   figsize, format, graph_num, no_plot, seed, verbose)
	gs.run()
	return gs


def prerank(rnk, gene_sets, outdir='GSEA_Prerank', pheno_pos='Pos', pheno_neg='Neg',
			min_size=15, max_size=500, permutation_num=1000, weighted_score_type=1,
			ascending=False, processes=1, figsize=(6.5,6), mpl_format='pdf',
			graph_num=20, no_plot=False, seed=None, verbose=False):
	""" Run Gene Set Enrichment Analysis with pre-ranked correlation defined by user.

	:param rnk: pre-ranked correlation table or pandas DataFrame. Same input with ``GSEA`` .rnk file.
	:param gene_sets: Enrichr Library name or .gmt gene sets file. Same input with GSEA.
	:param outdir: results output directory.
	:param int permutation_num: Number of permutations for significance computation. Default: 1000.
	:param int min_size: Minimum allowed number of genes from gene set also the data set. Defaut: 15.
	:param int max_size: Maximum allowed number of genes from gene set also the data set. Defaults: 500.
	:param str weighted_score_type: Refer to :func:`algorithm.enrichment_socre`. Default:1.
	:param bool ascending: Sorting order of rankings. Default: False.
	:param int processes: Number of Processes you are going to use. Default: 1.
	:param list figsize: Matplotlib figsize, accept a tuple or list, e.g. [width,height]. Default: [6.5,6].
	:param str mpl_format: Matplotlib figure format. Default: 'pdf'.
	:param int graph_num: Plot graphs for top sets of each phenotype.
	:param bool no_plot: if equal to True, no figure will be draw. Default: False.
	:param seed: Random seed. expect an integer. Default:None.
	:param bool verbose: Bool, increase output verbosity, print out progress of your job, Default: False.

	:returns: Return a Prerank obj. All results stored to a dictionary, obj.results, 
		where contains::

			| {es: enrichment score,
			|  nes: normalized enrichment score,
			|  p: P-value,
			|  fdr: FDR,
			|  size: gene set size,
			|  matched_size: genes matched to the data,
			|  genes: gene names from the data set}

	"""
	pre = Prerank(rnk, gene_sets, outdir, pheno_pos, pheno_neg,
				  min_size, max_size, permutation_num, weighted_score_type,
				  ascending, processes, figsize, mpl_format, graph_num, no_plot, seed, verbose)
	pre.run()
	return pre


def incontext(rnk, gene_sets, background_rnks, outdir='GSEA_PEN', pheno_pos='Pos', pheno_neg='Neg',
			min_size=15, max_size=500, permutation_num=1000, weighted_score_type=1,
			ascending=False, processes=1, figsize=(6.5,6), mpl_format='pdf',
			graph_num=20, no_plot=False, seed=None, verbose=False):
	""" Run GSEA-InContext, which is GSEAPreranked but using a background set of experiments defined by user.

	:param rnk: pre-ranked correlation table or pandas DataFrame. Same input as ``GSEA`` .rnk file.
	:param gene_sets: Enrichr Library name or .gmt gene sets file. Same input as GSEA.
	:param background_rnks: directory path or pandas DataFrame.

	:param outdir: results output directory.
	:param int permutation_num: Number of permutations for significance computation. Default: 1000.
	:param int min_size: Minimum allowed number of genes from gene set also the data set. Defaut: 15.
	:param int max_size: Maximum allowed number of genes from gene set also the data set. Defaults: 500.
	:param str weighted_score_type: Refer to :func:`algorithm.enrichment_socre`. Default:1.
	:param bool ascending: Sorting order of rankings. Default: False.
	:param int processes: Number of Processes you are going to use. Default: 1.
	:param list figsize: Matplotlib figsize, accept a tuple or list, e.g. [width,height]. Default: [6.5,6].
	:param str mpl_format: Matplotlib figure format. Default: 'pdf'.
	:param int graph_num: Plot graphs for top sets of each phenotype.
	:param bool no_plot: if equal to True, no figure will be draw. Default: False.
	:param seed: Random seed. expect an integer. Default:None.
	:param bool verbose: Bool, increase output verbosity, print out progress of your job, Default: False.

	:returns: Return a Prerank obj. All results stored to a dictionary, obj.results, 
		where contains::

			| {es: enrichment score,
			| nes: normalized enrichment score,
			| p: P-value,
			| fdr: FDR,
			| size: gene set size,
			| matched_size: genes matched to the data,
			| genes: gene names from the data set}
	"""
	ic = GSEA_InContext(rnk, gene_sets, background_rnks, outdir, pheno_pos, pheno_neg,
				  min_size, max_size, permutation_num, weighted_score_type,
				  ascending, processes, figsize, mpl_format, graph_num, no_plot, seed, verbose)
	ic.run()
	return ic


def ssgsea(data, gene_sets, outdir="ssGSEA_", sample_norm_method='rank', min_size=15, max_size=2000,
		   permutation_num=0, weighted_score_type=0.25, scale=True, ascending=False, processes=1,
		   figsize=(7,6), format='pdf', graph_num=20, no_plot=False, seed=None, verbose=False):
	"""Run Gene Set Enrichment Analysis with single sample GSEA tool.

	:param data: expression table, pd.Series, pd.DataFrame, GCT file, or .rnk file format.
	:param gene_sets: Enrichr Library name or .gmt gene sets file. Same input with GSEA.
	:param outdir: results output directory.
	:param str sample_norm_method: "Sample normalization method. Choose from {'rank', 'log', 'log_rank'}. Default: rank.

		1. 'rank': Rank your expression data, and transformed by 10000*rank_dat/gene_numbers
		2. 'log' : Do not rank, but transformed data by log(data + exp(1)), while  data = data[data<1] =1.
		3. 'log_rank': Rank your expression data, and transformed by log(10000*rank_dat/gene_numbers+ exp(1))
		4. 'custom': Do nothing, and use your own rank value to calculate enrichment score.
			See here: https://github.com/GSEA-MSigDB/ssGSEAProjection-gpmodule/blob/master/src/ssGSEAProjection.Library.R, line 86

	:param int min_size: Minimum allowed number of genes from gene set also the data set. Default: 15.
	:param int max_size: Maximum allowed number of genes from gene set also the data set. Default: 2000.
	:param int permutation_num: Number of permutations for significance computation. Default: 0.
	:param str weighted_score_type: Refer to :func:`algorithm.enrichment_score`. Default:0.25.
	:param bool scale: If True, normalize the scores by number of genes in the gene sets.
	:param bool ascending: Sorting order of rankings. Default: False.
	:param int processes: Number of Processes you are going to use. Default: 1.
	:param list figsize: Matplotlib figsize, accept a tuple or list, e.g. [width,height]. Default: [7,6].
	:param str format: Matplotlib figure format. Default: 'pdf'.
	:param int graph_num: Plot graphs for top sets of each phenotype.
	:param bool no_plot: if equal to True, no figure will be draw. Default: False.
	:param seed: Random seed. expect an integer. Default:None.
	:param bool verbose: Bool, increase output verbosity, print out progress of your job, Default: False.

	:returns: Return a ssGSEA obj. 
		All results store to  a dictionary, access enrichment score by obj.resultsOnSamples,
		and normalized enrichment score by obj.res2d.
		if permutation_num > 0, additional results contain::

			| {es: enrichment score,
			|  nes: normalized enrichment score,
			|  p: P-value,
			|  fdr: FDR,
			|  size: gene set size,
			|  matched_size: genes matched to the data,
			|  genes: gene names from the data set}
	"""
	ss = SingleSampleGSEA(data, gene_sets, outdir, sample_norm_method, min_size, max_size,
						  permutation_num, weighted_score_type, scale, ascending,
						  processes, figsize, format, graph_num, no_plot, seed, verbose)
	ss.run()
	return ss


def replot(indir, outdir='GSEA_Replot', weighted_score_type=1,
		   min_size=3, max_size=1000, figsize=(6.5,6), graph_num=20, format='pdf', verbose=False):
	"""Reproduce GSEA desktop outputs.

	:param indir: GSEA desktop results directory. In the sub folder, you must contain edb file foder.
	:param outdir: Output directory.
	:param float weighted_score_type: weighted score type. choose from {0,1,1.5,2}. Default: 1.
	:param list figsize: matplotlib output figure figsize. Default: [6.5,6].
	:param str format: matplotlib output figure format. Default: 'pdf'.
	:param int min_size: min size of input genes presented in Gene Sets. Default: 3.
	:param int max_size: max size of input genes presented in Gene Sets. Default: 5000.
		Not recommended to use min_size, or max_size argument in :func:`replot` function
		because gmt file has already been filtered.
	:param verbose: Bool, increase output verbosity, print out progress of your job, Default: False.

	:returns: Generate new figures with selected figure format. Default: 'pdf'.
	"""
	rep = Replot(indir, outdir, weighted_score_type,
				 min_size, max_size, figsize, graph_num, format, verbose)
	rep.run()

	return
