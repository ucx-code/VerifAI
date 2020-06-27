import pandas as pd 
from pickle import dump,load
import random
import numpy as np

from results import print_results

from grace import grace
from pursuit import pursuit
from timi import timi
from confidence import within_confidence_region_spin, within_confidence_region_python, explain_negative_spin 

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import f1_score,recall_score,matthews_corrcoef

from sklearn.tree import DecisionTreeClassifier
#from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
#import eli5

from imblearn.over_sampling import SMOTE, RandomOverSampler

class Timi:
    def fit(self,x,y):
        return

    def predict(self,X):
        return [timi(x,['SEX','Age','Enrl','RF','CCS>II','DEP ST','SBP','HR','KILLIP','hr','TN','Creat','CAA','AAS','Angina','Kn. CAD']) for x in X]

class Pursuit:
    def fit(self,x,y):
        return

    def predict(self,X):
        return [pursuit(x,['SEX','Age','Enrl','RF','CCS>II','DEP ST','SBP','HR','KILLIP','hr','TN','Creat','CAA','AAS','Angina','Kn. CAD']) for x in X]

if __name__=='__main__':

    #sets_on= [6,6,8,8,9,9,3,3]
    sets_on= [4,4,5,5,3,3,1]
    
    #DEFINE EXPERIMENT PARAMETERS
    runs=50 #to validate performance results
    seeds= load(open('seeds','rb')) #to allow same results
    #set random seed to the last (never used in the runs)
    random.seed(seeds[-1])   
    np.random.seed(seeds[-1])
    
    parameters_tunning=True
    train_on_wrong=False
    training_oversampler=SMOTE #can be SMOTE, RandomOverSampler, None
    
    confidence_function= within_confidence_region_python #using python for faster execution, or spin for the proposed framework
    event_threshold=40 #days 

    #DEFINE CLASSIFIERS PARAMETERS
    #Decision Tree
    dec_tre = DecisionTreeClassifier(criterion='gini', splitter='best', max_depth=10, min_samples_split=2, min_samples_leaf=2, min_weight_fraction_leaf=0.0, max_features='auto', random_state=None, max_leaf_nodes=None, min_impurity_decrease=0.0, min_impurity_split=None, class_weight={0: 1, 1: 5}, presort='deprecated', ccp_alpha=0.0)
    
    #logistic regressor
    #log = SGDClassifier(loss='log', penalty='l2', alpha=0.0001, l1_ratio=0.1, fit_intercept=True, max_iter=1000, tol=0.001, shuffle=True, verbose=0, epsilon=0.1, n_jobs=-1, random_state=None, learning_rate='optimal', eta0=0.0, power_t=0.5, early_stopping=False, validation_fraction=0.1, n_iter_no_change=5, class_weight=None, warm_start=False, average=False)
    
    log= LogisticRegression(penalty='l2', dual=False, tol=0.001, C=0.5, fit_intercept=True, intercept_scaling=1, class_weight=None, random_state=None, solver='liblinear', max_iter=1000, multi_class='auto', verbose=0, warm_start=False, n_jobs=None, l1_ratio=None)
    
    #KNNeighbors
    knn = KNeighborsClassifier(n_neighbors=5, weights='uniform', algorithm='ball_tree', leaf_size=30, p=2, metric='minkowski', metric_params=None, n_jobs=-1)    
    
    #Naive baise
    nb = GaussianNB(priors=None, var_smoothing=1e-09)
    
    #SVM
    svm=SVC(C=2.0, kernel='linear', degree=3, gamma='scale', coef0=0.0, shrinking=True, probability=False, tol=0.001, cache_size=200, class_weight=None, verbose=False, max_iter=-1, decision_function_shape='ovr', break_ties=False, random_state=None)
    
    #save references for the classifiers 
    models=[Pursuit(),Timi(),dec_tre,log,knn,nb,svm]
    m_labels=['Pursuit','Timi','DecTree','LogReg','Knn','Nb','SVM']
    
    #DEFINE METRICS STRUCTURES
    metrics={'Grace':{'f1':[],'se':[],'sp':[],'mcc':[],'g_count':[],'m_count':[],'t_count':[]}}
    for m in m_labels:
        metrics[m]={'f1':[],'se':[],'sp':[],'mcc':[]}
        metrics[m+'Hyb']={'f1':[],'se':[],'sp':[],'mcc':[]}
    
    
    print("####LOADING AND PREPROCESSING DATA####")
    #load data
    #file only has relevant data -> feature columns and Event days
    raw_data = pd.read_csv('data_raw.csv', sep=';')    
    
    #handle missing data -> substitute NaN for the median of the feature
    data = raw_data.fillna(raw_data.median().to_dict())
    
    #change event days to event class -> applying a mask to convert into a Binary classification problem
    data['Event'] = (data['Event'] < event_threshold).astype(int)
    
    #drop KILLIP or HF(signs) because they have .94 correlation
    #data= data.drop(columns='HF (signs)')
    
    #X and y
    X_data= data.drop(columns='Event').values.tolist()
    y_data= data['Event'].tolist() #also works .to_numpy()
    
    X_labels=['SEX','Age','Enrl','RF','CCS>II','DEP ST','SBP','HR','KILLIP','hr','TN','Creat','CAA','AAS','Angina','Kn. CAD']
    
    X_data, X_grid, y_data, y_grid = train_test_split( X_data, y_data, test_size=0.15, stratify=y_data)
    
    #CLASSIFIERS PARAMETERS TUNNING
    if parameters_tunning:
        
        #DEC TREE
        param_grid= {'criterion':('gini', 'entropy'), 'splitter':('best','random'), }
        GS= GridSearchCV(dec_tre, param_grid, scoring ='recall', n_jobs=-1, iid='deprecated', refit=True, cv=5, verbose=0, pre_dispatch='2*n_jobs')
        GS.fit(X_grid,y_grid)
        print(GS.best_estimator_)
        dec_tre= GS.best_estimator_
        
        #LINREG
        param_grid= {'solver':('liblinear','lbfgs','saga'),'C':(0.5,1,2)}
        GS= GridSearchCV(log, param_grid, scoring ='recall', n_jobs=-1, iid='deprecated', refit=True, cv=5, verbose=0, pre_dispatch='2*n_jobs')
        GS.fit(X_grid,y_grid)
        print(GS.best_estimator_)        
        log= GS.best_estimator_
        
        #KNN
        param_grid= {'n_neighbors':(5,10,15),'weights':('uniform','distance'), 'algorithm':('ball_tree','kd_tree')}
        GS= GridSearchCV(knn, param_grid, scoring ='recall', n_jobs=-1, iid='deprecated', refit=True, cv=5, verbose=0, pre_dispatch='2*n_jobs')
        GS.fit(X_grid,y_grid)
        print(GS.best_estimator_)      
        knn= GS.best_estimator_
        
        #SVM
        param_grid= {'kernel':('linear', 'poly', 'rbf', 'sigmoid'),'C':(0.5,1.0,2)}
        GS= GridSearchCV(svm, param_grid, scoring ='recall', n_jobs=-1, iid='deprecated', refit=True, cv=5, verbose=0, pre_dispatch='2*n_jobs')
        GS.fit(X_grid,y_grid)
        print(GS.best_estimator_)        
        svm= GS.best_estimator_
        
    print("####STARTING TRAINING AND TESTING####")
    #repeat n times:
    for run in range(runs):
        #setseed
        random.seed(seeds[run])
        np.random.seed(seeds[run])
        
        #split train test -> careful for having a stratified split
        _X_train, X_test, _y_train, y_test = train_test_split( X_data, y_data, test_size=0.39, stratify=y_data)        
        
        #add the grid search data to the training data
        _X_train= _X_train + X_grid
        _y_train= _y_train + y_grid
        
        
        if train_on_wrong:
            y_train_pred_grace = [grace(p,X_labels) for p in _X_train]
            _X_train=[x for x,y,yp in zip(_X_train,_y_train,y_train_pred_grace) if (y!=yp or y==1)]
            _y_train=[y for y,yp in zip(_y_train,y_train_pred_grace) if (y!=yp or y==1)] 
        
        #over/hybrid training sampling??
        if training_oversampler:
            X_train, y_train = training_oversampler().fit_resample(_X_train, _y_train) 
        else:
            X_train= _X_train
            y_train= _y_train
        
        #test grace
        y_test_pred_grace = [grace(p,X_labels) for p in X_test]
        #confidence assess grace
        assess = [confidence_function(p, X_labels, y_test_pred_grace[i], model=grace, range_params= sets_on) for i,p in enumerate(X_test)] 
        
        #metrics
        metrics['Grace']['t_count'].append(len(assess))
        metrics['Grace']['g_count'].append(sum(assess))
        metrics['Grace']['m_count'].append(len(assess) - sum(assess))
        
        #for each model
        for i,model in enumerate(models):
            
            #train
            model.fit(X_train,y_train)
            y_train_pred_model = model.predict(X_train) #for future stats
            
            #test
            y_test_pred_model = model.predict(X_test)
            y_test_pred_hybrid = []
            #Testing hybrid
            for j,(patient, y) in enumerate(zip(X_test,y_test)):
                print('\rStatus: Run:%d |Model:%s\t|Patient: %d/%d' % (run+1,m_labels[i],j,len(y_test)),end='')                
                
                if assess[j]:
                    y_test_pred_hybrid.append(y_test_pred_grace[j]) #risk_grace
                else:
                    y_test_pred_hybrid.append(y_test_pred_model[j]) #risk_model
            
            #calculate and store metrics
            metrics[m_labels[i]]['f1'].append(f1_score(y_test,y_test_pred_model))
            metrics[m_labels[i]]['se'].append(recall_score(y_test,y_test_pred_model))
            metrics[m_labels[i]]['sp'].append(recall_score(y_test,y_test_pred_model,pos_label=0))
            #metrics[m_labels[i]]['mcc'].append(matthews_corrcoef(y_test, y_test_pred_model))
            
            metrics[m_labels[i]+"Hyb"]['f1'].append(f1_score(y_test,y_test_pred_hybrid))
            metrics[m_labels[i]+"Hyb"]['se'].append(recall_score(y_test,y_test_pred_hybrid))
            metrics[m_labels[i]+"Hyb"]['sp'].append(recall_score(y_test,y_test_pred_hybrid,pos_label=0))            
            #metrics[m_labels[i]+"Hyb"]['mcc'].append(matthews_corrcoef(y_test, y_test_pred_model))
        
        #calculate and store grace metrics
        metrics['Grace']['f1'].append(f1_score(y_test,y_test_pred_grace))
        metrics['Grace']['se'].append(recall_score(y_test,y_test_pred_grace))
        metrics['Grace']['sp'].append(recall_score(y_test,y_test_pred_grace,pos_label=0))
        #metrics['Grace']['mcc'].append(matthews_corrcoef(y_test,y_test_pred_grace))
    
    print_results(metrics,sets_on)

    dump(metrics,open('results'+str(sets_on)+'.pickle','wb'))
