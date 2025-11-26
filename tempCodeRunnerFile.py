
#     def depositemoney(self):
#         accNO = input("Enter your account number:")
#         pin = int(input("Tell your pin:"))
#         user_data = [i for i in Bank.data if i["account No."] ==accNO and  i["pin"]==pin]
#         print(user_data)

#         if not user_data:
#             print("user not found")
        
#         else:
#             amount = int(input("Enter amount to be deposited:"))
#             if amount <= 0:
#                 print("Invalid amount")
#             elif amount > 10000:

#                 print("Greater than 10000")
#             else:
#                 user_data[0]["Balance"] += amount
#                 Bank.__update()
#                 print("Amount credited")
            
    
 
#     def withdrawmoney(self):
#         accNO = input("Enter your account number:")
#         pin = int(input("Tell your pin:"))
#         user_data = [i for i in Bank.data if i["account No."] ==accNO and  i["pin"]==pin]
#         print(user_data)

#         if not user_data:
#             print("user not found")
        
#         else:
#             amount = int(input("Enter amount to be withdraw:"))
#             if amount <= 0:
#                 print("Invalid amount")
#             elif amount > 10000:
#                 print("greater than 10000")

#                 print("Greater than 10000")

#             else:
#                 if user_data[0]["Balance"] < amount:
#                     print("Insufficient Balance")

#                 else:
#                     user_data[0]["Balance"]-= amount
#                     Bank.__update()
#                     print("Amount debited")

    
#     def details(self):
#         accNO = input("Enter your account number:")
#         pin = int(input("Tell your pin:"))
#         user_data = [i for i in Bank.data if i["account No."] ==accNO and  i["pin"]==pin]
        
#         if not user_data:
#             print("user not found")

#         else:
#             for i in user_data[0]:
#                 print(i,user_data[0][i])

    
    
#     def updatedetails(self):
#         accNO = input("Enter your account number:")
#         pin = int(input("Tell your pin:"))
#         user_data = [i for i in Bank.data if i["account No."] ==accNO and  i["pin"]==pin]
        
#         if not user_data:
#             print("user not found")
#         else:
#             print("youy cannot change Account Number")
#             print("Now update your details and skip it if you dont want to update")
#             #name,email,number,pin

#             new_data = {
#                 'name':input("Enter your new Name:"),
#                 'email':input("Enter your new email:"),
#                 'phone':int(input("Enter your new phone no.:")),
#                 'pin':int(input("Enter new pin:"))
#             }
            
#             for i in new_data:
#                 if new_data:
#                     new_data[i] = user_data[0][i]
#                     continue
#                 else:
#                     if new_data[i].isnumeric():
#                         user_data[0][i] = int(new_data[i])
#                     else:
#                         user_data[0][i] = new_data[i]
#             print(user_data)


#     def Delete(self):
#         accNO = input("please tell your account number ")
#         pin = int(input("please tell your pin aswell "))

#         userdata = [i for i in Bank.data if i['account No.'] == accNO and i['pin'] == pin]

#         if userdata == False:
#             print("sorry no such data exist ")
#         else:
#             check = input("press y if you actually want to delete the account or press n")
#             if check == 'n' or check == "N":
#                 print("bypassed")
#             else:
#                 index = Bank.data.index(userdata[0])
#                 Bank.data.pop(index)
#                 print("account deleted successfully ")
#                 Bank.__update()
        

            


        
            

# user = Bank()

# print("press 1 for creating an account")
# print("press 2 to deposite money")
# print("press 3 to withdraw money")
# print("press 4 for details")
# print("press 5 for updating the details")
# print("press 6 for deleting the account")




# check = int(input("tell your choice :-"))


# if check == 1:
#     user.createaccount()

# if check == 2:
#     user.depositemoney()

# if check == 3:
#     user.withdrawmoney()

# if check == 4:
#     user.details()


# if check == 5:
#     user.updatedetails()

# if check == 6:
#     user.Delete()