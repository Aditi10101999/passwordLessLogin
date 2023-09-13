# database
import psycopg2


cur=None
con=None


def connect_to_db(hostname, database,username, password, port_id):
    # db credentials
    hostname = hostname
    database = database
    username = username
    password = password
    port_id = port_id
    
    
    con = psycopg2.connect(host=hostname, dbname=database,
                            user=username, password=password, port=port_id)
    cur = con.cursor()    
    return [cur,con]
                                                        


def select_data(curr ,mob):
    select_query="select * from public.user_details where mobile_number='"+str(mob).replace('+','')+"'"
    curr.execute(select_query)
    select_output=curr.fetchall()

    return select_output



def insert_data(curr,conn,user_data):
    insert_query="INSERT INTO public.otp_data(id, mobile_number, otp) VALUES ('"+str(user_data[0])+"', '"+str(user_data[1])+"', '"+str(user_data[2])+"');"
    curr.execute(insert_query)
    conn.commit()



def select_otp_data(curr ,mob):
    select_query="select * from public.user_details where mobile_number='"+str(mob).replace('+','')+"'"
    curr.execute(select_query)
    select_output_otp=curr.fetchall()

    return select_output_otp
# select_data(connect_to_db('tools.neebal.com','pmi_db','pmi_web_user','G@Rtav#2x52f',7026))


def update_otp_data(curr,conn,mobile,otp):
    update_query="UPDATE public.otp_data SET otp='"+otp+"' WHERE mobile_number='"+mobile+"';"
    curr.execute(update_query)
    conn.commit()