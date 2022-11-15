import psycopg2
import psycopg2.extras
import shutil
import random as r
from fastapi import FastAPI, UploadFile, File
from fpdf import FPDF, HTMLMixin


class MyFPDF(FPDF, HTMLMixin):
    pass


# Details of the database
hostname = 'localhost'
database = 'postgres'
username = 'postgres'
pwd = "admin"
port_id = 5432

conn = None
cur = None

# Create a connection to the database
app = FastAPI()

# Create a table in the database


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    with open(f'{file.filename}', 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"filename": file.filename}


@app.post('/create_table')
async def root():
    conn = psycopg2.connect(
        host=hostname,
        dbname=database,
        user=username,
        password=pwd,
        port=port_id)

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    create_table = """
        CREATE TABLE IF NOT EXISTS test_table (
        index int,
        studentno int,
        lastname varchar(100),
        firstname varchar(100),
        middlename varchar(100),
        total int,
        cashcard varchar(100) NULL,
        college varchar(100),
        yrlvl varchar(100),
        course varchar(100),
        PRIMARY KEY (studentno)
        )
        """

    copy_table = """
        COPY test_table FROM 'C:\\Users\\adria\\Desktop\\SE_Files\\data_freshie_full.csv' DELIMITER ',' CSV HEADER;
    """

    select_table = """
        SELECT * FROM test_table;
    """

    cur.execute(create_table)
    cur.execute(copy_table)
    cur.execute(select_table)

    data = cur.fetchall()
    json_data = []
    for row in data:
        json_data.append(dict(row))

    print(json_data)

    conn.commit()
    conn.close()
    cur.close()

    return {'data': json_data}

# Delete a table in the database


@app.delete('/delete_table')
async def root():
    conn = psycopg2.connect(
        host=hostname,
        dbname=database,
        user=username,
        password=pwd,
        port=port_id)

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    delete_table = """
        DROP TABLE test_table;
    """

    cur.execute(delete_table)

    conn.commit()
    conn.close()
    cur.close()

    return {'data': 'Table Deleted'}


# Generate a PDF file
@app.get('/create_pdf')
async def root():
    conn = psycopg2.connect(
        host=hostname,
        dbname=database,
        user=username,
        password=pwd,
        port=port_id)

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute(
        'SELECT * FROM public.test_table'
    )

    pdf = MyFPDF(orientation='L', unit='mm', format='A4')
    pdf.add_page()
    pdf.set_font("helvetica", size=8)

    json_data = cur.fetchall()

    json_data.insert(0, [
        'index',
        'Student Number',
        'Last Name',
        'First Name',
        'Middle Name',
        'Total',
        'Cashcard',
        'College',
        'Year',
        'Course'
    ])

    # Convert all the content of json_data to string
    for row in json_data:
        for i in range(len(row)):
            row[i] = str(row[i])

    # """

    for row in json_data:
        pdf.write_html(
            f'<center><table width="100%"><tbody><tr><td width="10%">{row[1]}</td><td width="10%">{row[2]}</td><td width="20%">{row[3]}</td><td width="10%">{row[4]}</td><td width="5%">{row[5]}</td><td width="5%">{row[6]}</td><td width="5%">{row[7]}</td><td width="3%">{row[8]}</td><td width="5%">{row[9]}</td></tr></tbody></table></center>')

    # Random Generate a number for hash value
    hash_value = r.randint(1000000000, 9999999999)

    pdf.output(f'files/data-{hash_value}.pdf')

    conn.commit()
    conn.close()
    cur.close()

    return {'data': 'PDF Created'}

# View the table in the database


@app.get('/view_table')
async def root():
    conn = psycopg2.connect(
        host=hostname,
        dbname=database,
        user=username,
        password=pwd,
        port=port_id)

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute(
        'SELECT * FROM public.test_table'
    )

    data = cur.fetchall()
    json_data = []
    for row in data:
        json_data.append(dict(row))

    print(json_data)
    print(json_data[0])

    conn.commit()
    conn.close()
    cur.close()

    return {'data': json_data}
