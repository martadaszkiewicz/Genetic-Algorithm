def sequence_transformation(sequence,coordinates):
    transformed_sequence_coordinates = []
    for i in sequence:
        transformed_sequence_coordinates.append(coordinates[i])

    return transformed_sequence_coordinates
        
