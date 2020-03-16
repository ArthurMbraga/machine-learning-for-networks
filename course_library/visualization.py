import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
from sklearn.metrics import confusion_matrix
from sklearn.utils.multiclass import unique_labels

def plot_corr(df, width, height, print_value, thresh=0):
	    """ Plot a correlation plot
	    
	    Parameters
	    ------------
	    df: dataframe
			The dataframe of which we want to show 
			the correlation
	    width : int
	    	The width of the figure
	    height : int
	    	The height of the figure	    
	    print_value : bool
	    	If True, it prints the Pearson's 
	    	correlation coefficient values in 
	    	the picture
	    thresh : float
	    	No color will be shown if the correlation 
	    	value is below this threshold 
	    	in absolute value
	    """
	    cormat = df.corr()
	    cormat = cormat.where(abs(cormat)>=thresh)
	    cormat = cormat.fillna(0)
	    
	    mask = np.zeros_like(cormat, dtype=np.bool)
	    mask[np.triu_indices_from(mask)] = True
	    
	    # Inspired by https://stackoverflow.com/a/42977946/2110769
	    f, ax = plt.subplots(figsize=(width, height ) )
	    
	    # Inspired by https://medium.com/@chrisshaw982/seaborn-correlation-heatmaps-customized-10246f4f7f4b
	    sns.heatmap(cormat,
		    vmin=-1,
		    vmax=1,
		    cmap='coolwarm',
		    annot=print_value,
		       mask = mask);



def rotate_labels(sm):
		"""
		Rotate the labels of a scatter matrix

		Parameters
		-----------------
		sm: scatter matrix
		"""
		# source: https://stackoverflow.com/a/32568134/2110769
		[s.xaxis.label.set_rotation(45) for s in sm.reshape(-1)]
		[s.yaxis.label.set_rotation(0) for s in sm.reshape(-1)]
 

def plot_conf_mat(y_true, y_pred, class_names, normalize=False, title=None, 
			cmap=plt.cm.Blues):
 		"""
 		This function prints and plots the confusion matrix.
 		Normalization can be applied by setting `normalize=True`.

 		# Suppose target is the array of the true categories.
		# It contains as many values as the number of samples. Each value is an
		# integer number corresponding to a certain category. This array
		# represents the true category of each sample.
		#
		# predicted has the same format, but it does not represent the true
		# category, rather it represents the result of a model.
		#
		# Note in case of classification models, the categories are the classes,
		# while in case of anomaly detection models, the categories are
		# anomaly / normal
		#
 		"""
 		if not title:
 			if normalize:
 				title = 'Normalized confusion matrix'
 			else:
 				title = 'Confusion matrix, without normalization'

 		# Compute confusion matrix
 		cm = confusion_matrix(y_true, y_pred)

 		# Only use the labels that appear in the data
 		labels_present = unique_labels(y_true, y_pred)
 		classes = class_names[labels_present]
 		if normalize:
 			cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
 			print("Normalized confusion matrix")
 		else:
 			print('Confusion matrix, without normalization')

 		print(cm)

 		fig, ax = plt.subplots(figsize=(8,8))
 		im = ax.imshow(cm, interpolation='nearest', cmap=cmap)
 		ax.figure.colorbar(im, ax=ax)
 		# We want to show all ticks...
 		ax.set(xticks=np.arange(cm.shape[1]),
 			yticks=np.arange(cm.shape[0]),
 			# ... and label them with the respective list entries
 			xticklabels=classes, yticklabels=classes,
 			title=title,
 			ylabel='True label',
 			xlabel='Predicted label')

 		# Rotate the tick labels and set their alignment.
 		plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
 			rotation_mode="anchor")

 		# Loop over data dimensions and create text annotations.
 		fmt = '.2f' if normalize else 'd'
 		thresh = cm.max() / 2.
 		for i in range(cm.shape[0]):
 			for j in range(cm.shape[1]):
 				ax.text(j, i, format(cm[i, j], fmt),
 					ha="center", va="center",
 					color="white" if cm[i, j] > thresh else "black")
 		fig.tight_layout()
 		return ax
