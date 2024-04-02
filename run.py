from market import app #possible due to __init__ file as package(executes everything in the file a)

if __name__=='__main__': #checks if run.py has been executed
    app.run(debug=True) #pointer file for the importing and running and debug enables to not setup environment variable 