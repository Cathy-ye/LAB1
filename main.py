import pymysql


db_connect = pymysql.Connect(
                        host='127.0.0.1',
                        port=3306, #use port 3306 to connect to db
                        user='root',
                        passwd='asdfghjkl', #passwd here
                        db='lab1', #dbname
                        charset="utf8"
)

with db_connect:
    cursor = db_connect.cursor()

    sql = """CREATE TABLE IF NOT EXISTS`Papers`(
             `PaperID` varchar(255),
             `Title` longtext,
             `PaperPublishYear` varchar(255),
             `ConferenceID` varchar(255),
             PRIMARY KEY(`PaperID`)
             ); """
    cursor.execute(sql)

    sql = """CREATE TABLE IF NOT EXISTS`Authors`(
                     `AuthorID` varchar(255),
                     `AuthorName` varchar(255),
                     PRIMARY KEY(`AuthorID`)
                     ); """
    cursor.execute(sql)

    sql = """CREATE TABLE IF NOT EXISTS`Conferences`(
                            `ConferenceID` varchar(255),
                            `ConferenceName` varchar(255),
                            PRIMARY KEY(`ConferenceID`)
                             ); """
    cursor.execute(sql)

    sql = """CREATE TABLE IF NOT EXISTS`Affiliations`(
                            `AffiliationID` varchar(255),
                            `AffiliationName` varchar(255),
                             PRIMARY KEY(`AffiliationID`)
                            ); """
    cursor.execute(sql)

    sql = """CREATE TABLE IF NOT EXISTS`paper_author_affiliation`(
                            `id` int(6) NOT NULL auto_increment,
                            `PaperID` varchar(255),
                            `AuthorID` varchar(255),
                            `AffiliationID` varchar(255),
                            `AuthorSequence` varchar(255),
                            PRIMARY KEY (`id`)
                            ) ;"""
    # use a auto increment as primary key
    cursor.execute(sql)

    sql = """CREATE TABLE IF NOT EXISTS`paper_reference`(
                            `id` int NOT NULL auto_increment,
                            `PaperID` varchar(255),
                            `ReferenceID` varchar(255),
                            PRIMARY KEY(`id`)
                            ); """
    cursor.execute(sql)

    #set encoding=utf-8, or an error will occur
    with open('D:/python_projects/papers.txt',encoding='UTF-8') as f1:
        for line in f1:
            lines = line.strip().split('\t')
            #use strip() to remove \n at the end of the line
            print(lines)
            sql = """INSERT INTO Papers(PaperID,
                                    Title,
                                    PaperPublishYear,
                                   ConferenceID)
                    VALUES (%s,%s, %s, %s);"""
            cursor.execute(sql, lines)
            db_connect.commit()


    with open('D:/python_projects/authors.txt',encoding='UTF-8') as f2:
        for line in f2:
            lines = line.strip().split('\t')
            print(lines)
            sql = """INSERT INTO Authors(AuthorID,
                                            AuthorName)
                        VALUES (%s,%s);"""
            cursor.execute(sql, lines)
            db_connect.commit()

    with open('D:/python_projects/conferences.txt',encoding='UTF-8') as f3:
        for line in f3:
                lines = line.strip().split('\t')
                print(lines)
                sql = """INSERT INTO Conferences(ConferenceID,
                                            ConferenceName)
                        VALUES (%s,%s);"""
                cursor.execute(sql, lines)
                db_connect.commit()

    with open('D:/python_projects/affiliations.txt',encoding='UTF-8') as f4:
            for line in f4:
                lines = line.strip().split('\t')
                print(lines)
                sql = """INSERT INTO Affiliations(AffiliationID,AffiliationName)
                        VALUES (%s,%s);"""
                cursor.execute(sql, lines)
                db_connect.commit()


    with open('D:/python_projects/paper_author_affiliation.txt',encoding='UTF-8') as f5:
            for line in f5:
                lines = line.strip().split('\t')
                print(lines)
                sql = """INSERT INTO paper_author_affiliation(PaperID,
                                            AuthorID,
                                           AffiliationID,
                                            AuthorSequence)
                        VALUES (%s,%s, %s, %s);"""
                cursor.execute(sql, lines)
                db_connect.commit()


    with open('D:/python_projects/paper_reference.txt',encoding='UTF-8') as f6:
            for line in f6:
                lines = line.strip().split('\t')
                print(lines)
                sql = """INSERT INTO paper_reference(PaperID,
                                            ReferenceID)
                        VALUES (%s,%s);"""
                cursor.execute(sql, lines)
                db_connect.commit()

    # 给定论文ID 返回标题和发表年份
    sql = """
    SELECT Title, PaperPublishYear FROM Papers WHERE PaperID='58EA85EE';
    """
    cursor.execute(sql)

    #给定任意论文ID，返回该文章有多少citation
    sql = """
    SELECT count(*) FROM paper_reference 
    WHERE PaperID = '58EA85EE';
    """
    cursor.execute(sql)
    #给定任意论文ID，按照作者顺序返回各个作者ID
    sql = """
    SELECT AuthorID 
    FROM paper_author_affiliation WHERE PaperID = '58EA85EE' 
    ORDER BY AuthorSequence;
    """
    cursor.excute(sql)

    # 给定任意论文ID，按照作者顺序返回各个作者名字
    sql = """
    SELECT B.AuthorName
    FROM paper_author_affiliation A
    JOIN Authors B
    ON A.AuthorID = B.AuthorID
    WHERE PaperID = '58EA85EE' ORDER BY AuthorSequence;
    """
    cursor.execute(sql)

cursor.close()
db_connect.close()
