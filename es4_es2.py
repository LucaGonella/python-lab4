import sqlite3
from sys import argv
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

def print_sorted_list(bot, update):
    '''
    Print the elements of the list, sorted in alphabetic order
    '''
    sql="select * from task"
    connection = sqlite3.connect('task')
    cursor=connection.cursor()
    cursor.execute(sql)
    result =cursor.fetchall()
    print(result)
    cursor.close()
    message = ''
    # check if the list is empty
    if (len(tasks_list) == 0):
        message="Nothing to do, here!"
    else:
        # we don't want to modify the real list of elements: we want only to print it after sorting
        # there are 2 possibilities:
        # a) using the sort method
        #  temp_tasks_list = tasks_list[:]
        #  temp_tasks_list.sort()
        #  message = temp_tasks_list
        # b) using the sorted method (the sorted method returns a new list)
        message = sorted(tasks_list)
    bot.sendMessage(chat_id=update.message.chat_id, text=message)


# define one command handler. Command handlers usually take the two arguments:
# bot and update.
def start(bot, update):
    update.message.reply_text('Hello! This is AmITaskListBot. You can use one of the following commands:')
    update.message.reply_text('/newTask <task to add>')
    update.message.reply_text('/removeTask <task to remove>')
    update.message.reply_text('/removeAllTasks <substring used to remove all the tasks that contain it>')
    update.message.reply_text('/showTasks')

def echo(bot, update):
    # get the message from the user
    receivedText = update.message.text
    textToSend = "I'm sorry, I can't do that"
    bot.sendMessage(chat_id=update.message.chat_id, text=textToSend)

def saveListToFile():
    '''
    Here we save the changed list into the task_list.txt file
    '''
    filename = "task"
    try:
        # open file in write mode
        txt = open(filename, "w")

        # write each task as a new line in the file
        for single_task in tasks_list:
            txt.write(single_task + "\n")

        # close the file
        txt.close()
    except IOError:
        print("Problems in saving todo list to file")


if __name__ == '__main__':

    # main program

    # initialize the task list
    tasks_list = []
    # get the list from the "task_list.txt" file
    filename = "task"
    try:
        # open the file
        txt = open(filename)

        # read the file: load each row in an element of the list without "/n"
        tasks_list = txt.read().splitlines()

        # close the file
        txt.close()

    except IOError:
        # File not found! We work with an empty list
        print("File not found!")
        exit()

    updater = Updater(token='590898204:AAGnj2CzA2VTOUFeeycawi6VRuWOeddxkyA')

    # add an handler to start the bot replying with the list of available commands
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))

    # on non-command textual messages - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text, echo))

    # add an handler to insert a new task in the list
    newTask_handler = CommandHandler('newTask', new_task, pass_args=True)
    dispatcher.add_handler(newTask_handler)

    # add an handler to remove the first occurence of a specific task from the list
    removeTask_handler = CommandHandler('removeTask', remove_task, pass_args=True)
    dispatcher.add_handler(removeTask_handler)

    # add an handler to remove from the list all the existing tasks that contain a provided string
    removeAllTasks_handler = CommandHandler('removeAllTasks', remove_multiple_tasks, pass_args=True)
    dispatcher.add_handler(removeAllTasks_handler)

    # add an handler to show the list tasks
    showTasks_handler = CommandHandler('showTasks', print_sorted_list)
    dispatcher.add_handler(showTasks_handler)

    # run the bot
    updater.start_polling()

    # run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()
    connection.close()