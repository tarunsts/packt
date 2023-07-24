import requests as req
import datetime
import pandas as pd

# creating methods

def trend():
  tag=url+"2.3/tags"
  param={}
  print("If you want the Popular tag of all time then press 1 \nelse Provide the time period  in YYYY-MM-DD format")
  ip=input("Provide the start date or press 1\n")
  if (ip=="1"):
    param={
      "order":"desc",
      "sort":"popular",
      "site":"stackoverflow"
        }
  else:
    to_dt=input("provide the last date\n")

    dt=datetime.datetime.strptime(ip,'%Y-%m-%d')
    from_dt=int(dt.timestamp())

    dt=datetime.datetime.strptime(to_dt,'%Y-%m-%d')
    to_dt=int(dt.timestamp())
    if to_dt<from_dt:
      print("From date should be greater than To date")
      return 0
    param={
          "fromdate":from_dt,
          "todate":to_dt,
          "order":"desc",
          "sort":"popular",
          "site":"stackoverflow"
      }
  re=req.get(tag,params=param)
  #print(re.url)
  res=re.json()
  i=0
  popular_tag=[]
  while i<len(res['items']):
    popular_tag.append(res['items'][i]['name'])
    i=i+1
  df_tag=pd.DataFrame(popular_tag)
  return df_tag


def popular_question():

  pop_qt=url+'2.3/questions?order=desc&sort=votes&site=stackoverflow'
  #print(pop_qt)
  re=req.get(pop_qt)
  res=re.json()
  i=0
  df_qu=pd.DataFrame(columns=['Tag','Is_Answered','Question'])
  while i <len(res['items']):
    tag=res['items'][i]['tags']
    is_ans=res['items'][i]['is_answered']
    qu=res['items'][i]['title']
    t=','
    t=t.join(tag)
    df_qu.loc[i]=[t,is_ans,qu]
    i=i+1

  return df_qu

def search():

  search=url+"/2.3/search"
  quest=input("Enter your question\n")
  param={
      "order":"desc",
      "sort":"activity",
      "intitle":quest,
      "site":"stackoverflow"
  }
  re=req.get(search,params=param)
  #print(re.url)
  res=re.json()
  i=0
  ans={}
  while i <len(res['items']):
    if(res['items'][i]['is_answered']==True):
      ans[res['items'][i]['title']]=res['items'][i]['link']
    i=i+1
  df_ans=pd.DataFrame(ans.items())
  #print(ans)
  df_ans.columns=['Question','Answer']
  return df_ans



# creating main method

url=r'https://api.stackexchange.com/'
isUp=False
if(req.get(url).status_code==200):
  isUp=True


def main():
  if(isUp is False):
    print("Server is down or something wrong with the URL")
    return
  print('What you will like to do: ')
  print('\tPress 1 for Latest Trend\n\tPress 2 for searching an Answer\n\tPress any key to exist ')
  ip=input()
  if ip=='1':
    df_tag=trend()
    print(df_tag.head(3))
    df_tag.to_csv('Tag.csv')
  elif ip=='2':
    df_search=search()
    if len(df_search)>0:
      print('These are some question which we have found\n')
      print(df_search.head(3))
      df_search.to_csv('UserAnswer.csv')
    else:
      print("Sorry Did not found any Relevent Question")
  else :
    df_question=popular_question()
    print('Here some list of popular question')
    print(df_question.head())
    df_question.to_csv('Popular_Question.csv')
    print("\n\nThank You")

main()


