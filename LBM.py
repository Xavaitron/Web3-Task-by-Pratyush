from datetime import datetime,timedelta
import smtplib

#Creating a instance for sending email via Gmail(port 587)
s = smtplib.SMTP('smtp.gmail.com',587)
#start Transport layer security(TLS) for security
s.starttls()
#Logging a dummy gmail account to send mail from
s.login("web3dummy@gmail.com", "zgtc cmam dosw itlp")

class book:
    def __init__(self,title,author,publication_year,total_copies):
        self.title = title
        self.author = author
        self.publication_year = publication_year
        self.available_copies = total_copies 
        #initially nobody has checked out a book, so total = available
        self.total_copies = total_copies
        #no reservation has been done inititally
        self.reservation_by = None
    
    def check_out(self):
        #If there are available copies, it will decrease the quantity by 1
        if self.available_copies>0:
            self.available_copies-=1
        else:
            print(f"There are no available copies of {self.title} by '{self.author}'")

    def check_in(self):
        self.available_copies+=1
        #Remove reservation when it is checked in
        self.reservation_by = None

    def reservation(self,patron):

        if self.available_copies==0 and self.reservation_by==None:
            #Will reserve a book only if there are no available copies and it hasn't been reserved by anyone else
            self.reservation_by = patron
        elif self.reservation_by!=None:
            print(f"The book {self.title} has already been reserved by {self.reservation_by}")
        elif self.available_copies>0:
            print(f"There are available copies of {self.title} by '{self.author}'")
        else:
            print(f"There are no available copies of {self.title} by '{self.author}' for reservation")

class patron:
    def __init__(self,id,name,username,password,email):
        self.id = id
        self.name = name
        self.username = username
        self.password = password
        self.email = email
        #Inititally no book has been issued by the patron
        self.checked_out_books = []

    def authentication(self,username,password):
        if self.username == username and self.password == password:
            return True
    
    def check_out_book(self,book,username,password):

        #Raise an error if credentials do not match   
        if not self.authentication(username, password):
            raise Exception("Wrong Credentials")
        if book not in self.checked_out_books:
            self.checked_out_books.append(book)
            book.check_out()
            #Set the due date for the bbok
            issue_date = datetime.now()
            book.due_date = issue_date + timedelta(days=30)
            #Send Email(Google does not allow third party programs to send ails now due to security reasons)
            #Due to that I'm Commenting this code out
            # message = f"Book {book.title} by {book.author} has been checked out by {self.name} id:{self.id}"
            # s.sendmail("web3dummy@gmail.com", f"{self.email}", message)
            #Remove reservation if it was there
            if book.reservation_by == self:
                book.reservation_by = None
            #Store Transaction details
            transaction_instance = transaction(self, book, issue_date, "check_out")
        else:
            print(f"The book {book.title} has already been checked out by you")
    
    def return_book(self,book,username,password):

        #Checking Credentials  
        if not self.authentication(username,password):
            raise Exception("Wrong Credentials")
        #checks if the book is issued by the patron by looking in the list
        if book in self.checked_out_books:
            return_date = datetime.now()
            #inititalize late fees(it was popping an error if not done)
            late_fees = 0
            #finds difference between due date and return date in days and adds late fees to it if any
            if int((return_date-book.due_date).days)>0:
                late_fees += int((return_date - book.due_date).days)*100
            if late_fees >0:
                print(f"You have to pay late fees of {late_fees}")
            self.checked_out_books.remove(book)
            book.check_in()
            #store transaction details
            transaction_instance = transaction(self,book,return_date,"check_in")
            #Send Email
            # message = f"Book {book.title} by {book.author} has been checked in by {self.name} id:{self.id}"
            # s.sendmail("web3dummy@gmail.com", f"{self.email}", message)
        else:
            print(f"The book {book.title} hasn't been checked out by you")

class transaction:
    #each instance stores each transaction 
    def __init__(self,patron,book,date,type):
        self.patron = patron
        self.book = book
        self.date = date
        self.type = type

class branch:
    def __init__(self,branch_name):
        self.branch_name = branch_name
        self.books =[]
        self.patrons = []

    def add_book(self,book):
        self.books.append(book)

    def add_patron(self,patron):
        self.patrons.append(patron)

    def remove_patron(self,patron):
        if patron in self.patrons:
            self.patrons.remove(patron)
        else:
            print(f"The patron {patron} does not exist in patron database")
    
    def remove_book(self,book):
        if book in self.books:
            self.books.remove(book)
        else:
            print(f"The book {book} does not exist in the branch")

    def display_books(self):
        print(f"The Books in the {self.branch_name} Branch are:")
        for book in self.books:
            print(f"{book.title} by {book.author} has {book.available_copies} copies available.")

    def display_patrons(self):
        print(f"The Patrons in the {self.branch_name} Branch are:")
        for patron in self.patrons:
            print(f"{patron.name} ID:{patron.id}")

        
#Terminate SMTP Session
s.quit()



#Test code picked up online

# Creating instances of books
book1 = book("The Great Gatsby", "F. Scott Fitzgerald", 1925, 5)
book2 = book("To Kill a Mockingbird", "Harper Lee", 1960, 8)
book3 = book("1984", "George Orwell", 1949, 3)

# Creating instances of patrons
patron1 = patron(1, "Alice", "alice_username", "alice_password","ironpratyush@gmail.com")
patron2 = patron(2, "Bob", "bob_username", "bob_password","ironpratyush@gmail.com")

# Creating an instance of a branch
library_branch = branch("Main Library")

# Adding books to the branch
library_branch.add_book(book1)
library_branch.add_book(book2)
library_branch.add_book(book3)

# Adding patrons to the branch
library_branch.add_patron(patron1)
library_branch.add_patron(patron2)

# Displaying information about the branch and its books
library_branch.display_books()
library_branch.display_patrons()

patron1.check_out_book(book1, "alice_username", "alice_password")
patron2.check_out_book(book2, "bob_username", "bob_password")
patron2.check_out_book(book3, "bob_username", "bob_password")

# Displaying information about the branch after check-outs
library_branch.display_books()

# Attempting to return books
patron1.return_book(book2, "alice_username", "alice_password")
patron1.return_book(book1, "alice_username", "alice_password")

# Displaying information about the branch after returns
library_branch.display_books()