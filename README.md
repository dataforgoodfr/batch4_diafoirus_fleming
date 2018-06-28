# Team 3 - Fleming

<img src="http://www.sath.org.uk/edscot/www.educationscotland.gov.uk/Images/Alex%20Flemming_Penicillin%20L_tcm4-561885.jpg" width="300" alt="Alexander Fleming">

Named after Alexander Fleming (1881 - 1955), former Scottish physician, microbiologist, and pharmacologist, Nobel Prize 1945 in Physiology or Medicine, best known for discovering the lysozyme enzyme and the world's first antibiotic (Penicillin G).

The main goal of the project is to predict dynamically mortality risk for a given patient on a horizon of a few days.

## Meeting Notes
**04/04/2018**
- exploration des données, 
- discussions sur la manière de constituer les cohorts (âge, sexe, cholestérol moyen, fréquence cardiaque moyenne, pression artérielle moyenne, taille, poids, nb d'allergies, etc.), 
- stats importantes à obtenir: durée de séjours par unité (influence sur le nb d'observations), taux de mortalité et fréquence par diagnostics et par année, idem par unité, stats sur les indicateurs classiques par cohort.

**11/04/2018**
- Présentation des avantages du format OMOP: [format OMOP](https://github.com/MIT-LCP/mimic-omop)
- Possibilité de tester le format OMOP
- 


## TODO
- [ ] Accès à MIMIC PostGreS en python directement
- [ ] Benchmarker tous les indicateurs principaux (SOFA, IGS-II) et écrire des scripts pour les calculer.
- [ ] Réaliser un EDA complet (jupyter notebook) pour se faire une idée des biais existants (cf. idée de stats du 04/04)
- [ ] Avec ces résultats, créer nos propres indicateurs et en discuter avec le médecin référent (éventuellement les calculer sur des données d'hopitaux parisiens)
- [ ] Définir la mesure précise qu'on souhaite prédire (par itération sur la période temporelle entre autres)
- [ ] Benchmark des différents modèles suivant qq métriques dont: précision, nombre de variables explicatives, complexité d'entraînement du modèle (souci de reproductibilité).


## Relevant work

2011
- A Comparison of Intensive Care Unit Mortality Prediction Models through the Use of Data Mining Techniques (dec 2011): [paper](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3259558/)

2015
- Feature Representation for ICU Mortality (dec 2015): [paper](https://arxiv.org/abs/1512.05294)

2016
- Predicting Clinical Events by Combining Static and Dynamic Information Using Recurrent Neural Networks (feb 2016): [paper](https://arxiv.org/abs/1602.02685)
- Predicting ICU Mortality Risk by Grouping Temporal Trends from a Multivariate Panel of Physiologic Measurements  (feb 2016): [paper](https://pdfs.semanticscholar.org/2789/b71bf1e107f07317250519ad70667a10fe4d.pdf)
- Using recurrent neural network models for early detection of heart failure onset (aug 2016): [paper](https://academic.oup.com/jamia/article/24/2/361/2631499)
- Recurrent Neural Networks for Multivariate Time Series with Missing Values (nov 2016): [paper](https://arxiv.org/abs/1606.01865)
- Hospital Standardized Mortality Ratio (HSMR) (nov 2016): [paper](https://www.cihi.ca/sites/default/files/document/hsmr_tech_notes_en.pdf)

2017
- Dynamic Mortality Risk Predictions in Pediatric Critical Care Using Recurrent Neural Networks (jan 2017): [paper](https://arxiv.org/abs/1701.06675)
- Interpretable Deep Models for ICU Outcome Prediction (feb 2017): [paper](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5333206/)
- Generating Multi-label Discrete Patient Records using Generative Adversarial Networks (march 2017): [paper](https://arxiv.org/abs/1703.06490)
- Multitask Learning and Benchmarking with Clinical Time Series Data (march 2017): [paper](https://arxiv.org/abs/1703.07771), [repo](https://github.com/YerevaNN/mimic3-benchmarks)
- The Dependence of Machine Learning on Electronic Medical Record Quality (march 2017): [paper](https://arxiv.org/abs/1703.08251)
- PPMF: A Patient-based Predictive Modeling Framework for Early ICU Mortality Prediction (april 2017): [paper](https://arxiv.org/abs/1704.07499)
- Deep Learning to Attend to Risk in ICU (may 2017): [paper](https://arxiv.org/abs/1707.05010)
- Real time mortality prediction in the MIMIC-III database (july 2017): [repo](https://github.com/alistairewj/mortality-prediction)
- A review of modeling methods for predicting in-hospital mortality of patients in intensive care unit (august 2017): [paper](http://jeccm.amegroups.com/article/view/3790/4434)
- Mapping Patient Trajectories using Longitudinal Extraction and Deep Learning in the MIMIC-III Critical Care Database (august 2017): [paper](https://www.biorxiv.org/content/biorxiv/early/2017/08/17/177428.full.pdf)
- How To Predict ICU Mortality with Digital Health Data, DL4J, Apache Spark and Cloudera (sep 2017): [article](https://blog.cloudera.com/blog/2017/09/how-to-predict-icu-mortality-with-digital-health-data-dl4j-apache-spark-and-cloudera/)
- Early hospital mortality prediction of intensive care unit patients using an ensemble learning approach (oct 2017): [paper](https://www.sciencedirect.com/science/article/pii/S1386505617303581?via%3Dihub), [review](https://www.slideshare.net/RezaSadeghi4/early-hospital-mortality-prediction-of-intensive-care-unit-patients-using-an-ensemble-learning-approach)
- Benchmark of Deep Learning Models on Large Healthcare MIMIC Datasets (oct 2017): [paper](https://arxiv.org/abs/1710.08531)
- Real-time mortality prediction in the Intensive Care Unit (end of 2017): [paper](http://lcp.mit.edu/pdf/JohnsonAMIA2017.pdf)

2018
- Scalable and accurate deep learning for electronic health records (jan 2018): [paper](https://arxiv.org/abs/1801.07860)
- An Empirical Evaluation of Deep Learning for ICD-9 Code Assignment using MIMIC-III Clinical Notes (feb 2018): [paper](https://arxiv.org/abs/1802.02311)
- Deep Representation for Patient Visits from Electronic Health Records (march 2018): [paper](https://arxiv.org/abs/1803.09533)
- Memoire de stage - Prédiction mortalité sous 24h: [paper](https://www.researchgate.net/publication/325484454_L'apprentissage_profond_sur_MIMIC-III_Prediction_de_la_mortalite_sous_24_h) 

**Lectures**
- MIT 6.S897: Machine Learning for Healthcare [link](https://mlhc17mit.github.io/)


## Predictor candidates

- MEDS : [paper](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5357089/)
