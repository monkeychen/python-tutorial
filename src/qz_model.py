# -*- coding: utf-8 -*-

"""
Created on Thu May 30 12:37:21 2019

@author: zhanjiamei
"""
import pandas as pd
import numpy as np
from sklearn import metrics
import lightgbm as lgb  
from sklearn.model_selection import train_test_split  
from sklearn.linear_model import LogisticRegression
from sklearn import preprocessing
#from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
from sklearn.neural_network import MLPClassifier
from sklearn.externals import joblib
from sklearn.ensemble import AdaBoostClassifier
from scipy import stats



def lgb_train(traindata,trainlabel):
    X, val_X, y, val_y = train_test_split(traindata,trainlabel,test_size=0.05, random_state=0,stratify=trainlabel)  
    ## stratify=train_y 这里保证分割后y的比例分布与原数据一致  
    X_train = X  
    y_train = y  
    X_test = val_X  
    y_test = val_y  
    lgb_train = lgb.Dataset(X_train, y_train)  
    lgb_eval = lgb.Dataset(X_test, y_test, reference=lgb_train)  
# specify your configurations as a dict  
    params = {  
    'boosting_type': 'gbdt',  
    'objective': 'binary',  
    'metric': {'binary_logloss', 'auc'},  
    'num_leaves': 5,  
    'max_depth': 6,  
    'min_data_in_leaf': 450,  
    'learning_rate': 0.1,  
    'feature_fraction': 0.9,  
    'bagging_fraction': 0.95,  
    'bagging_freq': 5,  
    'lambda_l1': 1,    
    'lambda_l2': 0.001,  # 越小l2正则程度越高  
    'min_gain_to_split': 0.2,  
    'verbose': 5,  
    'is_unbalance': True  
    }    
# train  
    print('Start training...')  
    gbm = lgb.train(params,  
                lgb_train,  
                num_boost_round=500,  
                valid_sets=lgb_eval,  
                early_stopping_rounds=100)  
#    print('Save model...')  
    return gbm

def lgb_test(gbm,traindata):
#    gbm = lgb.Booster(model_file='model.txt')
    print('Start predicting...')  
    preds = gbm.predict(traindata, num_iteration=gbm.best_iteration)  # 输出的是概率结果  
    # 导出结果  
    q=[]
    threshold = 0.51  
    for pred in preds:  
        result = 1 if pred > threshold else 0
        q.append(result)   
    return preds,q


def rf_train_test(x,y,x2):
    clf = RandomForestClassifier(n_estimators=1000,min_samples_split=15, min_samples_leaf=10,  max_features='sqrt', random_state=0)
    clf.fit(x,y)#进行模型的训练
#    q2=clf.predict_proba(x2)
#    q1=clf.predict(x2)
    q_prob=clf.predict_proba(x2)
    q2=[]
    threshold = 0.5 
    for pred in q_prob:  
        result = 1 if pred[1] > threshold else 0
        q2.append(result)   
    return q2,clf


def read_csvdata(path,name):
    file = open(path+name,encoding='UTF-8')
    df=pd.read_csv(file)
    file.close()
    return df

#数据清洗 质差字段足够多且有效的样本
def dataclean(df):
    flag=pd.read_excel('D:\\pyfile\\qa_of_net\\数据补充2\\0603\\fi.xlsx',sheet_name='Sheet2',usecols ='B,F')
    flag2=flag[flag['c'].notnull()]       
    flag3=flag2.set_index(['字段名'])
    meanv0=df.mean()
    c = flag3.index
    u=df[c]
    undercount=np.zeros(len(u))
    for i in range(len(u)):
        item=u.iloc[i]
        notnancount=48-item.isna().sum()
#        nonc.append(notnancount)
        undercount[i]=0
        for j in c:
            standard=meanv0[j]        
            if ~np.isnan(item[j]):
                if flag3.loc[j]['c']==1 and item[j]<standard*0.8:
                    undercount[i]=undercount[i]+1
                elif flag3.loc[j]['c']==-1 and item[j]>standard*1.2:
                    undercount[i]=undercount[i]+1
        if notnancount!=0:
            undercount[i]=undercount[i]/notnancount
    print(len(df[undercount<=0.2])/len(df))
    return df[undercount<=0.2],df[undercount>0.2]

#数据清洗 质差字段足够多的样本
def dataclean2(df):
    zhicha_name=['is_bad_olt_pkt_drop_rate','is_bad_avg_http_browse_bigpkt_dl_rate','is_bad_sw_warning_lv2_count','is_bad_bras_warning_lv2_count','is_bad_avg_http_total_bigpkt_dl_rate','is_bad_avg_http_video_bigpkt_dl_rate',
       'is_bad_pon_terminal_type','is_bad_dns_success_rate','is_bad_avg_http_total_bigpkt_dl_rate_busy','is_bad_avg_http_browse_success_rate','is_bad_avg_http_browse_response_time','is_bad_avg_http_video_success_rate',
       'is_bad_avg_http_video_response_time','is_bad_avg_http_game_success_rate','is_bad_avg_http_game_bigpkt_dl_rate','is_bad_avg_http_game_response_time','is_bad_onu_rx_power','is_bad_pon_down_peak_utilization',
       'is_bad_pon_user_count','is_bad_olt_rx_power','is_bad_olt_up_peak_utilization','is_bad_olt_ping_delay','is_bad_olt_user_count','is_bad_olt_warning_lv1_count','is_bad_olt_warning_lv2_count','is_bad_sw_up_peak_utilization',
       'is_bad_sw_ping_delay','is_bad_sw_pkt_drop_rate','is_bad_sw_warning_lv1_count','is_bad_bras_up_peak_utilization','is_bad_bras_ping_delay','is_bad_bras_pkt_drop_rate','is_bad_bras_warning_lv1_count',
       'is_bad_avg_wifi_radio_power','is_bad_avg_subdevice_count','is_bad_auth_success_rate']    
    df2=df[zhicha_name]
#    df3=df2.replace(np.nan,-1)
    df3=pd.DataFrame()
    df3['nannum']=df2.isnull().sum(axis=1)
    df3['sum'] = df2.sum(skipna=True,axis=1)
    df3['rate1']=df3['sum']/36
    df3['rate2']=df3['sum']/(36-df3['nannum'])
    for col in zhicha_name:
        df[col]=df[col].fillna(0)
    return df,df3
    

    
path1='D:\\pyfile\\qa_of_net\\数据补充2\\0903\\6+8\\'

df_tousu=read_csvdata(path1,'tl6.csv')
df_tousu=df_tousu.drop(['max_field_count','sum_date','nai'],axis=1)
df_tousu['label']=1


df_feitousu =read_csvdata(path1,'nl6.csv')
df_feitousu =df_feitousu.drop(['max_field_count','sum_date','nai'],axis=1)
df_feitousu['label']=0

band_data = pd.concat([df_feitousu.sample(n=int(len(df_tousu)),random_state=1),df_tousu],axis=0,ignore_index=1)  
data=band_data.drop(['label'],axis=1)
label=band_data['label']


#3-fold
s0=np.random.permutation(range(data.shape[0]))
cut=int(len(s0)/3)
ll=[s0[i:i + cut] for i in range(0, len(s0), cut)]
l1=np.hstack((ll[0],ll[1]))
#l1=ll[0]
l2=ll[2]
traindata=data.iloc[l1]
trainlabel=label[l1]
testdata=data.iloc[l2]
testlabel=label[l2]
#空值填充
k=traindata.columns.tolist()
meanv=traindata.mean()
for col in traindata.columns:
    traindata[col].fillna(meanv[col],inplace=True)
    testdata[col].fillna(meanv[col],inplace=True)
#
#

''' 
gbm =lgb_train(traindata,trainlabel)
prob,q=lgb_test(gbm,testdata)
importance = gbm.feature_importance()  
names = testdata.columns
feature_importance = pd.DataFrame({'feature_name':names,'importance':importance} )
'''
#feature_importance.to_excel('noclean_feature_importance6.xlsx',index=False)
#import matplotlib.pyplot as plt
#ax = lgb.plot_tree(gbm, tree_index=3, figsize=(20, 8), show_info=['threshold'])
#plt.show()


q,clf=rf_train_test(traindata,trainlabel,testdata)
importance = clf.feature_importances_ 
names = testdata.columns
feature_importance = pd.DataFrame({'feature_name':names,'importance':importance} )


from sklearn.metrics import confusion_matrix
confmat = confusion_matrix(testlabel,q)
print(confmat)
from sklearn.metrics import classification_report
print(classification_report(testlabel,q))
print(confmat[0][0]/confmat[0].sum())
print(confmat[1][1]/confmat[1].sum())
print((confmat[0][0]+confmat[1][1])/confmat.sum())


#import pydotplus
#from IPython.display import Image
#dot_data = tree.export_graphviz(clf.estimators_[0], out_file='tree.dot', 
#                         feature_names=testdata.columns,  
#                         class_names=str(trainlabel.value_counts().index),  
#                         filled=True, rounded=True, special_characters=True)
#from subprocess import call
#call(['dot', '-Tpng','tree.dot', '-o', 'tree.png', '-Gdpi=600'])
#Image(filename ='tree.png')
#graph = pydotplus.graph_from_dot_data(dot_data)
#Image(graph.create_png())



#gbm.save_model('model1.txt')
#joblib.dump([meanv,k,gbm], "tl8.pkl")
        