CBP-SMF: an improved Semi-supervised Matrix tri-Factorization framework for characterizing Complex Biological Processes that represent sample groups 
=====================================================================================================================================================

Abstract
--------

**Motivation:** Matrix factorization techniques can integrative analysis
multi-dimensional genomic data across the same samples. We present
CBP-SMF, a framework for discovering complex biological processes (CBPs)
that underlying sample groups. Different from existing methods, CBP-SMF
is based on a de novo semi-supervised matrix tri-factorization that take
labeled samples as prior information, classify the unlabeled samples,
and devote to identify the underlying CBPs of groups.

**Methods:** CBP-SMF factorization decomposes several **non-negative
matrix Xi** into three matrices: **Molecular Coefficient Matrix Ui**,
**Factor Absorbing Wi**, **Sample Basis Matrix V**. We use euclidean
distance as cost function(so it's an optimization problem) to measure
the distance between Xi and reconstructed UiWiV. Besides, we incorporate
samples’ label information into NMF through a graph embedding constraint
and we give different input Xi a unique weight to donate its
contribution in optimization. Given input matrices Xi , labeled samples'
subgroup and a correlation matrix of labeled samples, CBP-SMF integrate
MG data (e.g., copy number variation, gene expression, microRNA
expression, and/or gene network) to classify the unlabeled samples into
groups and identify the underlying CBPs which characterize functional
properties of each group.

| **Results:** We evaluate CBP-SMF on breast cancer, classify unlabeled
  samples into four subtypes (Lumina A, Luminal B, Basal like, Her2) and
  highlight characteristic heterogeneous molecular pathways driving
  subtypes.
|  

The package
-----------

-  `**CBP\_SMF** <./CBP_SMF.py>`__ This software package contains all
   the functions of CBP-SMF.

Analysis scripts
----------------

-  `**BRCA\_example** <./BRCA_example.ipynb>`__ Run the CBP\_SMF package
   on BRCA's mRNA data and miRNA data.

Equations
---------

-  `**equations\_v044** <./equations_v044.ipynb>`__ This document
   contains equations of the algorithm. // to\_write

Figures
-------

+---------------------------------+
| |image0|                        |
+=================================+
| **Fig 1. CBP-SMF algorithm.**   |
+---------------------------------+

+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| |image1|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
+===================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================+
| **Fig 2. Classify samples into subgroup and implement KM survival analysis.** (A) KM survival curve for labeled samples. (B) KM survival analysis for unlabeled patients which are classified using CBP-SMF on mRNA expression and miRNA expression data. (C) KM survival analysis for unlabeled patients which are classified using CBP-SMF only on mRNA expression. (D) KM survival analysis for unlabeled patients which are classified on mRNA expression and miRNA expression data without graph embedding regularization.   |
+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| |image2|                                                                                                                                                                                                                                                                                                                                                                                                                 |
+==========================================================================================================================================================================================================================================================================================================================================================================================================================+
| **Fig 3. Complex Biological Processes that represent different samle groups.** We mapped the genes and miRNAs obtained from Luminal’s module and Basal-like’s module onto an integrated gene-regulation network.The network was obtained through integrating three databases including Reactom,KEGG and Nci Pathway Interaction Database. And the interactions between genes and miRNAs were obtained from miRTarBase.   |
+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

.. |image0| image:: E:\python code\github_package\CBP_SMF_package\images\algorithm.PNG
.. |image1| image:: E:\python code\github_package\CBP_SMF_package\images\Figure2_survival_4.1.PNG
.. |image2| image:: E:\python code\github_package\CBP_SMF_package\images\LB_Basal_module.PNG
