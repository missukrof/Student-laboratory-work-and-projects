import matplotlib.pyplot as plt
from sklearn import metrics

def plot_roc(test_label, preds_prob):

    # calculate the fpr and tpr for all thresholds of the classification
    fpr, tpr, threshold = metrics.roc_curve(test_label, preds_prob)
    roc_auc = metrics.auc(fpr, tpr)


    # plot auc
    plt.plot(fpr, tpr, 'b', label = 'AUC = %0.2f' % roc_auc)
    plt.plot([0, 1], [0, 1],'r--')

    plt.xlim([0, 1])
    plt.ylim([0, 1])

    plt.ylabel('True Positive Rate')
    plt.xlabel('False Positive Rate')

    plt.title('Receiver Operating Characteristic')

    plt.legend(loc = 'lower right')

    plt.show()
