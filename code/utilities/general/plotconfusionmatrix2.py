import matplotlib.pyplot as plt
import numpy as np
import itertools

def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45,fontsize=40)
    plt.yticks(tick_marks, classes,fontsize=40)

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, cm[i, j],
                 horizontalalignment="center",
                 verticalalignment="center",
                 color="white" if cm[i, j] > thresh else "black",fontsize=80)

    plt.tight_layout()
    plt.ylabel('True',fontsize=40)
    plt.xlabel('Predicted',fontsize=40)
    plt.show()

    tp = cm[1,1]
    fn = cm[1,0]
    fp = cm[0,1]
    tn = cm[0,0]
    
    if tp + fn == 0:
        print('Recall (Sensitivity) = Undefined (tp + fn = 0)')
    else:
        print('Recall (Sensitivity) =  {:.2f}'.format(tp / (tp + fn)))

    print('Specificity =     {:.2f}'.format(tn/(tn+fp)))
    print('Accuracy =     {:.2f}'.format((tp+tn)/(tp+fp+tn+fn)))
    print('Precision(PPV) =     {:.2f}'.format(tp/(tp+fp)))
    print('NPV =     {:.2f}'.format(tn/(tn+fn)))
    print('False positive rate  =     {:.2f}'.format(fp/(tn+fp)))
 