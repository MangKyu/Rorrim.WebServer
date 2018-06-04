import FaceID
if __name__ == '__main__':
    face_classification = FaceID.FaceID()
    #face_classification.start_training()
    file_name = 'test.jpg'
    uid = 'lion'
    uid_label, accuracy = face_classification.get_accrucy('test.jpg')
    if uid_label.__contains__(uid) and accuracy >= 0.9:
        print('Login Success')
    else:
        print('Login Fail')