from training_Validation_Insertion import train_validation


try:
    result_path='./data'
    train_valObj = train_validation(result_path)  # object initialization
    train_valObj.train_validation()

except ValueError:

    print("Error Occurred! %s" % ValueError)

except KeyError:

    print("Error Occurred! %s" % KeyError)

except Exception as e:

    print( 'Error Occurred! '+str(e))
print("validation is done!!")
 


