import mysql.connector
from config import dbargs


def sql_exec(sql):
    """
        W3SCHOOLS MYSQL CONNECTOR FOR MOR INFO
    """
    mydb = mysql.connector.connect(
        host=dbargs["host"],
        user=dbargs["user"],
        password=dbargs["password"],
        port=dbargs["port"],
        database=dbargs["database"],
        auth_plugin=dbargs["auth_plugin"]

    )
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    mydb.commit()
    mycursor.close()
    mydb.close()
def sql_select(sql):
    mydb = mysql.connector.connect(
        host=dbargs["host"],
        user=dbargs["user"],
        password=dbargs["password"],
        port=dbargs["port"],
        database=dbargs["database"],
        auth_plugin=dbargs["auth_plugin"]

    )
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    data = mycursor.fetchall()
    mycursor.close()
    mydb.close()
    return data
async def checkPerms(interaction, roleList):
    role_ids = [role.id for role in interaction.user.roles]
    for role in roleList:
        if role in role_ids:
            print("You're allowed")
            return True
    await interaction.response.send_message("You need to be a Mod or Admin in order to use this command!")
    return False
