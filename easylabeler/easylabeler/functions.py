from django.shortcuts import render
import requests


########################################################################################################
def runMLService(request):
	import pymysql
	import os
	from sklearn.model_selection import train_test_split
	from sklearn.metrics import accuracy_score, f1_score, confusion_matrix
	from sklearn import svm
	from nltk.corpus import stopwords
	from sklearn.feature_extraction.text import CountVectorizer
	from sklearn.feature_extraction.text import TfidfTransformer
	from joblib import dump, load
	import nltk
	
	stored_index = 0;
	dump(stored_index, "stored_index.joblib");
	
	# This line of code should be executed for only once.
	# nltk.download('stopwords')
	
	# Connect to the database
	conn = pymysql.connect(host = 'localhost'
	, user = 'root'
	, passwd ='root'
	, port = 8889 		# default is 3306, but should use 8889 here since I used a different port.
	, db = 'easyLabeler' 
	, charset = 'utf8' );
	
	cur = conn.cursor(); 
	sql = "select * from `tempdata`"; 
	cur.execute(sql)
	rawdata = cur.fetchall() 	# obtain the data by using fetchall
		
	data = [];
	labels = [];
	
	for i in rawdata:
		data.append(i[1]);
		labels.append(i[2]);
		
	X_train, X_test, y_train, y_test = train_test_split(data, labels, stratify=labels, test_size=0.25)
	# Here we do not need to consider the testing sets for generating the initial classifier
	
	# Preprocess the data
	count_vect = CountVectorizer(stop_words=stopwords.words('english'))
	count_vect.fit(X_train)
	dump(count_vect, "count_vect.joblib");
	X_train_counts = count_vect.transform(X_train)
	
	tfidf_transformer = TfidfTransformer(use_idf=True, sublinear_tf=True).fit(X_train_counts)
	dump(tfidf_transformer, "tfidf_transformer.joblib");
	X_train_tf = tfidf_transformer.transform(X_train_counts)
	
#	SVM = svm.SVC(C=1.0, kernel='linear', degree=3, gamma='auto')
	SVM = svm.LinearSVC()
	SVM.fit(X_train_tf, y_train);
	
	# Preprocess testing data
	X_new_counts = count_vect.transform(X_test)
	X_new_tfidf = tfidf_transformer.transform(X_new_counts)
	
	# predict the labels on validation dataset
	predictions_SVM = SVM.predict(X_new_tfidf)
	
	# Test and evaluate the trained model
	dump(len(confusion_matrix(y_test, predictions_SVM)), "classNumber.joblib")
#	print("SVM Accuracy Score -> ", accuracy_score(predictions_SVM, y_test))
	accuracy = "The classifier's accuracy is: " + str(round(accuracy_score(predictions_SVM, y_test),3))
#	print("SVM f1_score -> ", f1_score(y_test, predictions_SVM, pos_label=1))
	
	classifier = SVM;
	dump(classifier, "model.joblib");
	
	if (os.path.exists('model.joblib')):
		returnData = "Successfully generated the classifier.";
	else:
		returnData = "Sorry, failed to generate the classifier.";
	
	cur.close()
	conn.close()
	return render(request, 'generateClassifier.html', {'returnData':returnData, 'accuracy':accuracy})


########################################################################################################
def returnResults(request):
	import os
	from joblib import dump, load
	import pymysql
	from sklearn.model_selection import train_test_split
	from sklearn.metrics import accuracy_score, f1_score, confusion_matrix
	from sklearn import svm
	from nltk.corpus import stopwords
	from sklearn.feature_extraction.text import CountVectorizer
	from sklearn.feature_extraction.text import TfidfTransformer
	from joblib import dump, load
	import nltk
	import numpy as np
	
	# This line of code should be executed for only once.
	# nltk.download('stopwords')
	
	stored_index = 0;
	if (os.path.exists('stored_index.joblib')):
		stored_index = load("stored_index.joblib");
		
	returnData = "";
	if (os.path.exists('model.joblib')):
		loaded_classifier = load("model.joblib");
		loaded_count_vect = load("count_vect.joblib");
		loaded_tfidf_transformer = load("tfidf_transformer.joblib");
	else:
		returnData = "Sorry, you haven't generated the classifier. Please click the button above.";
		return render(request, 'generateClassifier.html', {'returnData2':returnData})
		
	#connect to the database
	conn = pymysql.connect(host = 'localhost'
	, user = 'root'
	, passwd ='root'
	, port = 8889 		# default is 3306, but should use 8889 here since I used a different port.
	, db = 'easyLabeler'
	, charset = 'utf8' );
	
	cur = conn.cursor(); 
	sql = "select * from `maindata`";
	cur.execute(sql)
	rawdata = cur.fetchall() 	# obtain the data by using fetchall
		
	data = [];
	labels = [];
	
	for i in rawdata:
		data.append(i[2]);
		
	# Preprocess the data
	X_train_counts = loaded_count_vect.transform(data)
	X_train_tf = loaded_tfidf_transformer.transform(X_train_counts)
	X_train_tf_dense = X_train_tf.todense()
	
	if (os.path.exists('classNumber.joblib')):
		numOfClass = load("classNumber.joblib");
		
	
	information_dict = {}
	for i in range(0, len(X_train_tf_dense)):
		y = abs(loaded_classifier.decision_function(X_train_tf_dense[i]))
		w_norm = np.linalg.norm(loaded_classifier.coef_)
		dist = y / w_norm
		if (numOfClass == 2):
			information_dict.update({i:dist[0]})
		else:	#for number of classes which is >= 3
			information_dict.update({i:min(dist[0])})
	
	# Do sorting based on the distance from closest to farthest
	sorted_dict = sorted(information_dict.items(), key = lambda kv:(kv[1], kv[0]))

	temp_index = sorted_dict[stored_index][0]
	returnData = data[temp_index];
	
	stored_index = stored_index + 1;
	dump(stored_index, "stored_index.joblib");
	
	cur.close()
	conn.close()
	return render(request, 'generateClassifier.html', {'returnData2':returnData})
	

########################################################################################################
def handleFormData(request):
	import pymysql
	
	# Connect to the database
	conn = pymysql.connect(host = 'localhost'
	, user = 'root'
	, passwd ='root'
	, port = 8889 		# default is 3306, but should use 8889 here since I used a different port.
	, db = 'easyLabeler' 
	, charset = 'utf8' );
	
	cur = conn.cursor(); 
	
	choice = request.GET['choice']
	text = request.GET['textarea']
	slashes_text = text.replace("'", "\\'")		# This way is very clever
	returnData = "";
	
	if (text == ""):
		returnData = "Labeled failed! You haven't chosen any text to label.";
		return render(request, 'generateClassifier.html', {'returnData3':returnData})
	
	if (choice == ""):
		returnData = "Labeled failed! You haven't labeled the text. Please give the text a label.";
		return render(request, 'generateClassifier.html', {'returnData3':returnData})
	
	sql = "SELECT * FROM `tempdata` WHERE content = " + '\'' +  slashes_text + '\''
	cur.execute(sql)
	rawdata = cur.fetchall() 	# obtain the data by using fetchall
	
	if (rawdata):
		returnData = "Labeled failed! You have already labeled this text. Please change another.";
		return render(request, 'generateClassifier.html', {'returnData3':returnData})
	
	sql = "SELECT * FROM `returnData` WHERE content = " + '\'' +  slashes_text + '\''
	cur.execute(sql)
	rawdata = cur.fetchall() 	# obtain the data by using fetchall
	
	if (rawdata):
		returnData = "Labeled failed! You have already labeled this text. Please change another.";
		return render(request, 'generateClassifier.html', {'returnData3':returnData})
			
#	if (choice == "negative"):
#		sql = "INSERT INTO `tempdata`(content, label) VALUES (" + '\'' + slashes_text + '\'' + ", 0)";
#		cur.execute(sql)
#		conn.commit()
#		sql = "INSERT INTO `returnData`(content, label) VALUES (" + '\'' + slashes_text + '\'' + ", 0)";
#		cur.execute(sql)
#		conn.commit()
#		returnData = "Labeled successfully! You can continue do labeling by clicking the button above."
#
#	elif (choice == "positive"):
#		sql = "INSERT INTO `tempdata`(content, label) VALUES (" + '\'' + slashes_text + '\'' + ", 1)";
#		cur.execute(sql)
#		conn.commit()
#		sql = "INSERT INTO `returnData`(content, label) VALUES (" + '\'' + slashes_text + '\'' + ", 1)";
#		cur.execute(sql)
#		conn.commit()
#		returnData = "Labeled successfully! You can continue do labeling by clicking the button above."
	
	sql = "INSERT INTO `tempdata`(content, label) VALUES (" + '\'' + slashes_text + '\'' + "," + choice + ")";
	cur.execute(sql)
	conn.commit()
	sql = "INSERT INTO `returnData`(content, label) VALUES (" + '\'' + slashes_text + '\'' + "," + choice + ")";
	cur.execute(sql)
	conn.commit()
	returnData = "Labeled successfully! You can continue to do labeling by clicking the button above."
	
	sql = "SELECT * FROM `maindata`" 
	cur.execute(sql)
	rawdata = cur.fetchall() 	# obtain the data by using fetchall
	total = len(rawdata)
	
	sql = "SELECT * FROM `tempdata`" 
	cur.execute(sql)
	rawdata = cur.fetchall() 	# obtain the data by using fetchall
	labeled = len(rawdata)
	
	content = "You have labeled " + str(labeled) + " out of " + str(total) + " texts.";
					
	return render(request, 'generateClassifier.html', {'returnData3':returnData, 'returnData':content})


########################################################################################################
def generateLabeledFiles(request):
	import pymysql
	import os
	import shutil
	from joblib import dump
	
	dump(0, "stored_index2.joblib");
	
	# Connect to the database
	conn = pymysql.connect(host = 'localhost'
	, user = 'root'
	, passwd ='root'
	, port = 8889 		# default is 3306, but should use 8889 here since I used a different port.
	, db = 'easyLabeler' 
	, charset = 'utf8' );
	
	cur = conn.cursor(); 
	sql = "select * from `returnData`"; 
	cur.execute(sql)
	rawdata = cur.fetchall() 	# obtain the data by using fetchall
	
	if os.path.exists("labeled_data"):
		shutil.rmtree("labeled_data")
		
	os.mkdir("labeled_data")
	
	returnData = "Sorry. Failed to generate the labeled files."
	
	for i in rawdata:
		with open("labeled_data/file_" + str(i[0]) + "_label_" + str(i[2]) + ".txt","w") as f:
			f.write(i[1]);
			returnData = "Congratulations. Successfully generated the labeled files."
	
	
	return render(request, 'generateClassifier.html', {'returnData4': returnData})


########################################################################################################
def checkLabeledData(request):
	import pymysql
	import os
	from joblib import dump, load
	
	# Connect to the database
	conn = pymysql.connect(host = 'localhost'
	, user = 'root'
	, passwd ='root'
	, port = 8889 		# default is 3306, but should use 8889 here since I used a different port.
	, db = 'easyLabeler' 
	, charset = 'utf8' );
	
	cur = conn.cursor(); 
	sql = "select * from `returnData`"; 
	cur.execute(sql)
	rawdata = cur.fetchall() 	# obtain the data by using fetchall
	
	stored_index2 = 0;
	if (os.path.exists('stored_index2.joblib')):
		stored_index2 = load("stored_index2.joblib");
	
	if (stored_index2 < len(rawdata)):
		label = rawdata[stored_index2][2];
		hint = "You have labeled " + str(label) + " for the following text:"
		text = rawdata[stored_index2][1];
		stored_index2 = stored_index2 + 1;
		dump(stored_index2, "stored_index2.joblib");
		
		return render(request, 'generateClassifier.html', {'returnData5': text, 'returnData7': hint})
	
	else:
		returnData = "You have already checked all the labeled texts. Please generate those labeled files."
		return render(request, 'generateClassifier.html', {'returnData6': returnData})
	
	
########################################################################################################
def handleChangedData(request):
	import pymysql
	
	# Connect to the database
	conn = pymysql.connect(host = 'localhost'
	, user = 'root'
	, passwd ='root'
	, port = 8889 		# default is 3306, but should use 8889 here since I used a different port.
	, db = 'easyLabeler' 
	, charset = 'utf8' );
	
	cur = conn.cursor(); 
	
	choice = request.GET['choice2']
	text = request.GET['textarea2']
	slashes_text = text.replace("'", "\\'")		# This way is very clever
	returnData = "";
	
	if (text == ""):
		returnData = "Confirm change failed! You haven't chosen any text to change its label.";
		return render(request, 'generateClassifier.html', {'returnData6':returnData})
	
	if (choice == ""):
		returnData = "Confirm change failed! You haven't labeled the text. Please label the text again.";
		return render(request, 'generateClassifier.html', {'returnData6':returnData})
	
		
	sql = "SELECT * FROM `returnData` WHERE content = " + '\'' +  slashes_text + '\''
	cur.execute(sql)
	rawdata = cur.fetchall() 	# obtain the data by using fetchall
	
	if (rawdata):
		sql = "DELETE FROM `returnData` WHERE content = " + '\'' +  slashes_text + '\''
		cur.execute(sql)
		conn.commit()
		
		sql = "INSERT INTO `returnData`(content, label) VALUES (" + '\'' + slashes_text + '\'' + "," + choice + ")";
		cur.execute(sql)
		conn.commit()
		
		returnData = "Changed successfully! You can continue to check texts by clicking the button above."
		
		return render(request, 'generateClassifier.html', {'returnData6':returnData})
	