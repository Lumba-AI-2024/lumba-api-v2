        datasetname=request.query_params['datasetname'],
    if 'selected_columns' not in request.query_params:
        preproceess = Preprocess(dataset=dataset)
        result = preproceess.data_duplication_check()
        return Response(result, status=status.HTTP_200_OK)
    columns = request.query_params['selected_columns']
    columns = columns.split(",")
    preproceess = Preprocess(dataframe=dataframe, columns=columns)
    return Response(result, status=status.HTTP_200_OK)

        datasetname=request.query_params['datasetname'],
    if 'selected_columns' not in request.query_params:
        dataframe = pd.read_csv(dataset.file)
        preproceess = Preprocess(dataframe=dataframe)
        result = preproceess.data_duplication_check()
        return Response(result, status=status.HTTP_200_OK)
    columns = request.query_params['selected_columns']
    columns = columns.split(",")
    preproceess = Preprocess(dataframe=dataframe, columns=columns)
    return Response(result, status=status.HTTP_200_OK)

        datasetname=request.query_params['datasetname'],
    preproceess = Preprocess(dataset=dataset)
    return Response(result, status=status.HTTP_200_OK)

        datasetname=request.query_params['datasetname'],
    return Response(result, status=status.HTTP_200_OK)

        datasetname=request.query_params['datasetname'],
    if 'selected_columns' not in request.query_params:
        preproceess = Preprocess(dataset=dataset)
        result = preproceess.data_duplication_check()
        return Response(result, status=status.HTTP_200_OK)
    columns = request.query_params['selected_columns']
    columns = columns.split(",")
    preproceess = Preprocess(dataset=dataset, columns=columns)
    return Response(result, status=status.HTTP_200_OK)

        datasetname=request.query_params['datasetname'],
    preproceess = Preprocess(dataset=dataset)

        datasetname=request.data['datasetname'],
    preprocess = Preprocess(dataset=dataset)
    print(request.data.dict())
    payload = preprocess.handle(**request.data.dict())


    print(request.data)
        file_name = request.data['datasetname']
        datasetname=request.data['datasetname'],
    columns=request.data['selectedTrainingColumns']
    columns = columns.split(",")
    preprocess = Preprocess(dataset=dataset, columns=columns)



    # create new file model with serializer


