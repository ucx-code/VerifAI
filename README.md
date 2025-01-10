# Verifiable-AI

Intelligent software systems are increasingly being used in critical domains like the medical health care.
Artificial Intelligence in general, and Machine Learning in particular, pose new challenges to Verification, a crucial step of the critical systems development process.
Formal Methods, such as Model Checking, are well known techniques that allow for proving properties in critical systems.

Current work assesses the usage of Model Checking to perform verification in an emergency hospital patients risk assessment use case, [integrating with the LORE explainer](https://kdd.isti.cnr.it/cre_vue/\#/).

The proposed approach is a framework that contemplates verification steps during both design and run time. 
In specific, at design-time, it is able to check a model for invalid end states, non-determinism and accordance with \textit{a priori} knowledge.
Online verification focus on verifying the confidence of a classification (forecasting) for a specific instance, based on a tailored distance measure that checks the closeness to the model decision boundaries. 
This last phase of verification is also considered as ensemble strategy in a scenario of combining more than one classifier.  

Experimentation was done on three available risk assessment models (the Risk Scores GRACE, PURSUIT and TIMI) with real data of 460 hospital patients. 
Verification at design-time for the three models (a) confirmed the inexistence of invalid end states for the whole operation input space nor (b) non-determinism for the available test set, and (c) provided confirmation of compliance with \textit{a priori} knowledge statements. 
Online verification (performed for GRACE) successfully divided the available instances (patients) into two groups, \textit{Confident} and \textit{Not-confident} about the risk assessment, where (a) the performance in comparison to the baseline improved for the \textit{Confident} group and degraded for the \textit{Not-confident} one, and (b) the execution statistics of the model checker proved its efficiency to perform verification at run time. 
The ensemble strategy was evaluated in two scenarios that considered different overall usage ratios for the verified GRACE model (based on the online verification parametrisation), along with several complementary classifiers. PURSUIT, one of the domain dependent Risk Scores, and a trained Decision Tree Classifier provided the best match to complement GRACE in the classification of instances not-confidently assessed. 

Based on the results, the proposed framework succeeds in using Model Checking for verification to increase trust on intelligent systems decisions, made in critical domains.
