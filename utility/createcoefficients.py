import json

def main():
    coefficients = {
        'stat_typing_atk':1,
        'stat_typing_def':1,
        'stat_':1
        }

    print('Utility : Create coefficients.json')
    print()
    print('What preset would you like the json to have?')
    print('\t[1] Default')
    print('\t[2] Custom')
    print()

    while True:
        choice = input('Enter your choice :')

        if choice.isdigit():
            choice = int(choice)
        else:
            print('Please enter respective number to continue')
            print()

        if not choice in range(1,3):
            print('Please enter number within the range')
        else:
            break

    print()

    if choice == 1:
        mode = 'Default'

    elif choice == 2:
        mode = 'Custom'
        for key in coefficients:
            while True:
                value = input(f'Please enter {key} value :')

                if value.isdigit() or value.isfloat():
                    value = int(choice)
                    coefficients[key] = value
                    print()
                    break

                else:
                    print('Input a number')
                    print()

    with open('coefficients.json','w') as f:
        json.dump(coefficients ,f ,indent=3)


    print(f'Successfully saved the json file with {mode} preset')
    input('Press any key to exit')

if __name__ == '__main__':
    main()
