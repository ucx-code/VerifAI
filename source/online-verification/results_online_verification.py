from pickle import load
from sklearn.metrics import f1_score,recall_score,accuracy_score
from statistics import mean


def print_results(y_true, y_pred):
	
    print('F1',round(f1_score(y_true,y_pred),6),end=' ')

    print('|| Accuracy',round(accuracy_score(y_true,y_pred),6),end=' ')
    
    #recall as SENSITIVITY    
    print('|| Sensitivity',round(recall_score(y_true,y_pred),6),end=' ')
    
    #recall as SPECIFICITY
    print('|| Specificity',round(recall_score(y_true,y_pred, pos_label=0),6))
    
if __name__=='__main__':

	print(None)