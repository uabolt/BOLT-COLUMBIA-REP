''' This file has some auxiliary functions for the catalog '''

def seems_legit_answers(pos, reph):
    ''' Returns true if the answers look legit for both sets of annotations '''

    return pos_seems_legit(pos) and reph_seems_legit(reph)

def pos_seems_legit(annotations):
    ''' See if the submissions look legitimate or not. It is only a hint '''

    # First extract the answers as a list of tuples
    answers = annotations.values('legible', 'guess', 'question', 'continue_process')

    empty = 0.
    repeated = {}

    res = True

    if len(answers) > 0:

        for i in answers:

            guess = i['guess'].strip()
            question = i['question'].strip()

            if not (guess or question):
                # Check for empty annotaitons
                empty += 1
            else:

                # Accumulate repeated values
                tup = (guess, question)

                if tup in repeated:
                    repeated[tup] += 1
                else:
                    repeated[tup] = 1.



        if empty / len(answers) > .3:
            res &= False
        else:
            res &= True

        vals = repeated.values()

        if len(vals) > 0 and (max(vals) / len(answers) > .3):
            res &= False
        else:
            res &= True

    else:
        res &= False

    return res

def reph_seems_legit(annotations):
    ''' See if the submissions look legitimate or not. It is only a hint '''

    # First extract the answers as a list of tuples
    answers = annotations.values('local_rephrase', 'local_merge', 'global_rephrase')

    empty = 0.
    repeated = {}

    res = True

    if len(answers) > 0:

        for i in answers:

            local_rephrase = i['local_rephrase'].strip()
            local_merge = i['local_merge'].strip()
            global_rephrase = i['global_rephrase'].strip()


            if not (local_rephrase or local_merge or global_rephrase):
                # Check for empty annotaitons
                empty += 1
            else:

                # Accumulate repeated values
                tup = (local_rephrase, local_merge, global_rephrase)

                if tup in repeated:
                    repeated[tup] += 1
                else:
                    repeated[tup] = 1.



        if empty / len(answers) > .3:
            res &= False
        else:
            res &= True

        vals = repeated.values()

        if len(vals) > 0 and (max(vals) / len(answers) > .3):
            res &= False
        else:
            res &= True

    else:
        res &= False

    return res
