import mysql.connector



def makeCon():
    #Goal of the function is to make a returnable connection 
    conn = None
    try:  
        conn = mysql.connector.connect(
            host='localhost',
            user='engradmin',
            password='temp1234',
            database='engrDisp'
        )
    except Exception as error:
        print("Error in databaseCon.py with makeCon: ", type(error).__name__, "–", error)
    
    return conn
#makeCon()

def getImages():
    #Goal is to retrive all of the data from the database
    rows = None
    try:
        #Getting and formatting the connection for the right query
        conn = makeCon()
        if conn == None:
            print()
        else:
            cur = conn.cursor(dictionary=True)
            query = "Select * FROM dispTable"
            cur.execute(query)
            rows = cur.fetchall()
            
            #Display all the info for testing
            for row in rows:
                print(row)
                
            #Clean up connections
            cur.close()
        conn.close()
    except Exception as error:
        print("Error in databaseCon.py with getImages: ", type(error).__name__, "–", error)
    
    return rows    
#getImages()

def getTableSize():
    #Goal is to get the total size of the table
    total_rows = None
    try: 
        
        #Making the connection and query
        conn= makeCon()
        if conn == None:
            print()
            
        else:
            cur = conn.cursor(dictionary=True)
            query = "select count(*) from dispTable"
            cur.execute(query)
            res = cur.fetchall()
                    
            #Checking if a value was gotten
            if res and res[0] is not None:
                total_rows = res[0]
                #print(total_rows)
            else:
                print("resultes value was null in databaseCon.py getTableSize")

            #Cleaning up tables
            cur.close()
            
        conn.close()
        
    except Exception as error:
        print("Error in databaseCon.py with getTableSize: ", type(error).__name__, "–", error)
        
    return total_rows
    
#getTableSize()

def getActive():
    #Goal is to get all the images with the active tag on them 
    res = None
    try:
        #Making the connection and query 
        conn = makeCon()
        if( conn == None):
            print()
        else:
            
            #Making the query
            cur = conn.cursor(dictionary=True)
            query = "Select * from dispTable where imgActive = TRUE"
            
            cur.execute(query)
            res = cur.fetchall()
            
            if len(res) == 0:
                print("No values found")
            #Uncomment to test
            #print(res)
            
            
            #Cleaning up the connections
            cur.close()
        
        conn.close()
        
    except Exception as error:
        print("Error in databaseCon.py with getActive: ", type(error).__name__, "–", error)
        
    return res
#getActive()


def getInactive():
    #Goal is to get all the images with the inactive tag on them 
    res = None
    try:
        #Making the connection
        conn = makeCon()
        if (conn == None):
            print("No connection")
        else:
            
            #Making the query
            cur = conn.cursor(dictionary=True)
            query = "Select * from dispTable where imgActive = FALSE"
            
            cur.execute(query)
            res = cur.fetchall()
            
            if len(res) == 0:
                print("No inactive values")
            #Uncomment to test
            #print(res)
            
            
            #Cleaning up connections
            cur.close()
        
        conn.close()
        
    except Exception as error:
        print("Error in databaseCon.py with getActive: ", type(error).__name__, "–", error)
        
    return res
#getInactive()


    
    
def changeActive(imgName, status):
    #Goal is to swap the image active status
    try:
        conn = makeCon()
        if( conn == None):
            print()
        else:
            cur = conn.cursor(dictionary=True)
            query = "Select * from dispTable where imgName = %s"
            
            cur.execute(query, (imgName,))
            res = cur.fetchall()
            
            if len(res) == 0:
                print("Found no values")
            else:
                #Need to change the value and resend it 
                update_query = "update dispTable set imgActive = %s where imgName = %s"
                cur.execute(update_query, (status, imgName))
                
                #Commit the changes
                conn.commit()
    except Exception as error:
        print("Error in databaseCon.py with changeActive: ", type(error).__name__, "–", error)
                
            