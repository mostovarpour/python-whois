import pymysql.cursors

# variables for our mysql connection
MYSQL_HOST = 'localhost'
MYSQL_USER = 'python_user'
MYSQL_PASS = 'icann'
MYSQL_DB = 'python_db'
MYSQL_CHARSET = 'utf8mb4'


def insert_ip(ip, registrant_contact, admin_contact, tech_contact):
    mysql_connection = pymysql.connect(host=MYSQL_HOST,
                                    user=MYSQL_USER,
                                    password=MYSQL_PASS,
                                    db=MYSQL_DB,
                                    charset=MYSQL_CHARSET,
                                    cursorclass=pymysql.cursors.DictCursor)
    try:
        with mysql_connection.cursor() as cursor:
            sql = "INSERT INTO `ips` (`ip_address`, `registrant_contact`, `admin_contact`, `tech_contact`) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (ip, registrant_contact, admin_contact, tech_contact))
            mysql_connection.commit()
    except:
        print("Something went wrong inserting an IP into the database")
    mysql_connection.close()


def insert_domain(domain, registrant_contact, admin_contact, tech_contact):
    mysql_connection = pymysql.connect(host=MYSQL_HOST,
                                    user=MYSQL_USER,
                                    password=MYSQL_PASS,
                                    db=MYSQL_DB,
                                    charset=MYSQL_CHARSET,
                                    cursorclass=pymysql.cursors.DictCursor)
    try:
        with mysql_connection.cursor() as cursor:
            sql = "INSERT INTO `domains` (`domain_name`, `registrant_contact`, `admin_contact`, `tech_contact`) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (domain, registrant_contact, admin_contact, tech_contact))
            mysql_connection.commit()
    # finally:
    except:
        print("Something went wrong inserting a domain into the database")
    mysql_connection.close()


def read_ip(ip):
    mysql_connection = pymysql.connect(host=MYSQL_HOST,
                                    user=MYSQL_USER,
                                    password=MYSQL_PASS,
                                    db=MYSQL_DB,
                                    charset=MYSQL_CHARSET,
                                    cursorclass=pymysql.cursors.DictCursor)
    try:
        with mysql_connection.cursor() as cursor:
            sql = "SELECT `ip_address`, `registrant_contact`, `admin_contact`, `tech_contact` FROM `ips` where `ip_address`=%s"
            cursor.execute(sql, (ip))
            result = cursor.fetchone()
            return result
    except:
        print("Something went wront reading an IP from the database")
    mysql_connection.close()


def read_domain(domain):
    mysql_connection = pymysql.connect(host=MYSQL_HOST,
                                    user=MYSQL_USER,
                                    password=MYSQL_PASS,
                                    db=MYSQL_DB,
                                    charset=MYSQL_CHARSET,
                                    cursorclass=pymysql.cursors.DictCursor)
    try:
        with mysql_connection.cursor() as cursor:
            sql = "SELECT `domain_name`, `registrant_contact`, `admin_contact`, `tech_contact` FROM `domains` where `domain_name`=%s"
            cursor.execute(sql, (domain))
            result = cursor.fetchone()
            return result
    except:
        print("Something went wrong read a domain from the database")
    mysql_connection.close()


if __name__ == "__main__":
    ip_address = read_ip('10.0.0.0')
    print("Testing 10.0.0.0: " )
    print(ip_address["ip_address"])
    print("\n")
    # domain_name = read_domain('test0.com')
    # print(domain_name)
    # for i in range(10):
    #     insert_domain(('test' + str(i) + '.com'), 'matthew.ostovarpour@icann.org', 'matthew.ostovarpour@icann.org', 'matthew.ostovarpour@icann.org')