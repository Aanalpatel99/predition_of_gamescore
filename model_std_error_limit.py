import mysql.connector

cnx = mysql.connector.connect(user='root', password='mysql21',
                              host='127.0.0.1',
                              port=3306,
                              database='gamescore')

cur=cnx.cursor()

def prediction(score): #function for predict cheat in games
    score= int(score)
    score=score**2# print(score)
    no_of_games=int(dataList[4])
    sum_of_score=int(dataList[3])

    scorePerGame=score/no_of_games# print(scorePerGame)
    i=scorePerGame-sum_of_score
    i=abs(i)#print(i)

    std_error=(i*no_of_games)/(no_of_games-1)
    std_error=std_error**0.5# print(std_error)

    assumedScore=std_error-scorePerGame# print(assumedScore)
    assumedScore=abs(assumedScore)
    return(assumedScore)

def increament(sum_of_score,no_of_games):#function for incrementing sum and game played
    sum_of_score=int(sum_of_score)
    sum_of_score+=newScore# print(sum_of_score)
    query="Update error set sum_of_score =%s where userid =%s"
    input_data=(sum_of_score,playerId)
    cur.execute(query,input_data)

    no_of_games=int(no_of_games)
    no_of_games+=1# print(no_of_games)
    query="Update error set no_of_games_played =%s where userid =%s"
    input_data=(no_of_games,playerId)
    cur.execute(query,input_data)

def change_score(newScore,highScore,lowScore):#function for changing high and low score in db
    highScore=int(highScore)
    lowScore=int(lowScore)
    if newScore>highScore:
        query="Update error set high_score =%s where userid =%s"
        input_data=(newScore,playerId)
        cur.execute(query,input_data)
    elif newScore<lowScore:
        query="Update error set low_score =%s where userid =%s"
        input_data=(newScore,playerId)
        cur.execute(query,input_data)
    else:
        pass


query="USE gamescore ;"
cur.execute(query)

query="SELECT * FROM error;"
cur.execute(query)

results=cur.fetchall()
for i in results:
    print(i)

playerId=input("user_id= ")# print(userId)
gameId=input("game_id= ")# print(gameId)
newScore=input("new_score= ")
newScore=int(newScore)# print(newScore)


for x in results:
    if playerId not in x:
        pass
    else:
        dataUser=x;# print(dataUser)

dataList=list(dataUser) #convert tuple into list
# print(dataList)


lowLimit=prediction(dataList[5])# print(lowLimit)
highLimit=prediction(dataList[6])# print(highLimit)


if  newScore<highLimit:
    query="Update error set score =%s where userid =%s"
    input_data=(newScore,playerId)
    cur.execute(query,input_data)
    increament(dataList[3],dataList[4])# argument sequance=sum of scores,num of games palyed
    change_score(newScore,dataList[6],dataList[5])# argument sequance= newscore,hoghscore,lowscore
else:
    print("cheat detected")



cur.close()
cnx.commit()
cnx.close()
