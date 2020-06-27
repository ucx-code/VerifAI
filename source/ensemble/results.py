import matplotlib.pyplot as plt
import numpy as np

def print_results(metrics,sets_on):

    print('\n####RESULTS AND STATS####')
    
    #present data
    #3 figures of box plots
    _labels= metrics.keys()

    labels=[l for l in metrics.keys() if l.find('Grace') >= 0 or l.find('Hyb') > 0]
    
    print('f1 hybrid',[(k,round(np.mean(metrics[k]['f1']),4)) for k in labels])
    print('se hybrid',[(k,round(np.mean(metrics[k]['se']),4)) for k in labels])
    print('sp hybrid',[(k,round(np.mean(metrics[k]['sp']),4)) for k in labels])
    #print('mcc',[(k,np.mean(metrics[k]['mcc'])) for k in labels])
    
    print('Grace avg usage:',np.mean(metrics['Grace']['g_count'])/metrics['Grace']['t_count'][0])
    
    fig1,(ax1,ax2,ax3)=plt.subplots(3,1,figsize=(10,20))
    #fig,(ax2,ax3)=plt.subplots(1,2,figsize=(10,5))
    
    #fig1, ax1 = plt.subplots(figsize=(10,5),dpi=300)
    ax1.set_title('F1 score | Hybrid Approaches')
    ax1.boxplot([metrics[k]['f1'] for k in labels], labels=labels,whis=2)   
    ax1.tick_params(axis='x', labelrotation=25)
    ax1.set_ylim(0,0.35)
    
    #fig2, ax2 = plt.subplots(figsize=(10,5),dpi=300)
    ax2.set_title('Sensitivity | Hybrid Approaches')
    ax2.boxplot([metrics[k]['se'] for k in labels], labels=labels,whis=2)#whis=2
    ax2.tick_params(axis='x', labelrotation=25)
    ax2.set_ylim(0,1.1)
    
    #fig3, ax3 = plt.subplots(figsize=(10,5),dpi=300)
    ax3.set_title('Specificity | Hybrid Approaches')
    ax3.boxplot([metrics[k]['sp'] for k in labels], labels=labels,whis=2)
    ax3.tick_params(axis='x', labelrotation=25)
    ax3.set_ylim(0,1.1)    
    
    fig1.savefig('f1_hyb_'+str(sets_on)+'.png')
    #fig2.savefig('se_hyb_'+str(sets_on)+'.png')
    #fig3.savefig('sp_hyb_'+str(sets_on)+'.png')

    #present data
    #3 figures of box plots
    labels=[l for l in metrics.keys() if l.find('Hyb') < 0]

    print('f1 single',[(k,round(np.mean(metrics[k]['f1']),4)) for k in labels])
    print('se single',[(k,round(np.mean(metrics[k]['se']),4)) for k in labels])
    print('sp single',[(k,round(np.mean(metrics[k]['sp']),4)) for k in labels])
    
    fig1, ax1 = plt.subplots(figsize=(10,10),dpi=300)
    ax1.set_title('F1 score | Individual Classifiers')
    ax1.boxplot([metrics[k]['f1'] for k in labels], labels=labels,whis=2)   
    ax1.tick_params(axis='x', labelrotation=25)
    ax1.set_ylim(0,0.35)
    
    fig2, ax2 = plt.subplots(figsize=(5,10),dpi=300)
    ax2.set_title('Sensitivity | Individual Classifiers')
    ax2.boxplot([metrics[k]['se'] for k in labels], labels=labels,whis=2)
    ax2.tick_params(axis='x', labelrotation=25)
    ax2.set_ylim(0.0,1.1)
    
    fig3, ax3 = plt.subplots(figsize=(7,5),dpi=300)
    ax3.set_title('Specificity | Individual Classifiers')
    ax3.boxplot([metrics[k]['sp'] for k in labels], labels=labels,whis=2)
    ax3.tick_params(axis='x', labelrotation=25)
    ax3.set_ylim(0.0,1.1)    
    
    fig1.savefig('f1_sin_.png')
    fig2.savefig('se_sin_.png')
    fig3.savefig('sp_sin_.png')


if __name__=='__main__':
    from pickle import load

    #sets_on= [4,4,5,5,3,3,1,1]
    sets_on= [6,6,8,8,9,9,3,3]

    print(sets_on)
    metrics= load(open('results'+str(sets_on)+'.pickle','rb'))

    sets_on ='test'
    print_results(metrics, sets_on)

    labels=[l for l in metrics.keys() if l.find('Grace') >= 0 or l.find('Hyb') > 0]

    print('f1 hybrid\n',[print(round(np.mean(metrics[k]['f1']),4)) for k in labels])
    print('se hybrid\n',[print(round(np.mean(metrics[k]['se']),4)) for k in labels])
    print('sp hybrid\n',[print(round(np.mean(metrics[k]['sp']),4)) for k in labels])

    labels=[l for l in metrics.keys() if l.find('Hyb') < 0]

    print('f1 single\n',[print(round(np.mean(metrics[k]['f1']),4)) for k in labels])
    print('se single\n',[print(round(np.mean(metrics[k]['se']),4)) for k in labels])
    print('sp single\n',[print(round(np.mean(metrics[k]['sp']),4)) for k in labels])

