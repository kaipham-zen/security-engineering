import matplotlib.pyplot as plt
import string


def analyse_frequency(ct,key_length=16):
    """Store chars based on their corresponding index of the repeating key
    and analyse frequencies of each list to observe the shift like Caesar Cipher"""
    # Create key_length substitution lists
    subs_list = [[] for i in range(key_length)]

    # Group characters based on their index of the repeating key
    for i,chr in enumerate(ct):
        index = i % key_length
        subs_list[index].append(chr)
    
    # Frequency analysis for each sub list
    subs_frequency = []

    for list in subs_list:
        # Create dictionary for alphabet [A-Z] with count=0
        frq = {i:0 for i in string.ascii_uppercase}
        
        # Count number of chars in sub list
        for char in list:
            frq[char] += 1
        
        subs_frequency.append(frq)
    
    return subs_frequency

def frequency_plot(subs_frequency):
    # Plotting frequency chart for each list
    for i, sub_frequency in enumerate(subs_frequency):        
        plt.bar(list(sub_frequency.keys()), list(sub_frequency.values()), color='b')
        plt.suptitle(f'Sub list at key\'s index {i}')
        plt.xlabel('Symbol')
        plt.ylabel('Frequency')
    
        plt.show()

def vigenere(ct,k):
    k = k.upper()
    pt = ""

    for i, ct_chr in enumerate(ct):
        if ct_chr in string.ascii_uppercase:
            # Get the key letter to decrypt the corresponding ciphertext letter
            k_chr = k[i%len(k)]
            # Shift A-Z 65-90 to 0-25
            k_shift = ord(k_chr) - ord('A')
            ct_shift = ord(ct_chr) - ord('A')
            # Vigenere decrypt function
            pt_chr_shift = (ct_shift - k_shift) % 26
            # Shift back and convert to ASCII representation
            pt_chr = chr(pt_chr_shift + ord('A'))
            
            # Append decrypted plaintext to plaintext variable (pt)
            pt += pt_chr
        else:
            # Non-alphabetical character are kept the same and appended to pt
            pt += ct_chr        

    return pt

def main():
    # Read file and extract the ciphertext
    ct_file = "ciphertext.txt"
    with open(ct_file,'r') as f:
        ct = f.readline()

    # Store the index and characters of non-alphabetical characters
    non_alpha = []
    for i, ct_chr in enumerate(ct):
        if ct_chr not in string.ascii_uppercase:
            non_alpha.append((i,ct_chr))
            # Remove non-alphabetical characters from ciphertext
            ct = ct.replace(ct_chr,"")

    ### Toggle comment the frequency analysis part (between ###) for testing decryption key
    # Perform frequency analysis
    print("\nAnalysing frequency...")
    print(f"\nCiphertext(non-alphabet removed):\n{ct}")
    subs_frequency = analyse_frequency(ct)
    
    # Plot the frequencies
    frequency_plot(subs_frequency)
    ### Toggle comment the frequency analysis part (between ###) for testing decryption key
    

    print("\nStarting to decrypt...")
    # Manually enter key and call vigenere function with input key and ciphertext to decrypt
    while True:
        # Prompt user to input key
        k = input("\nEnter key (enter 'q' to exit): ")
        if k == 'q':
            break
        pt = vigenere(ct,k)
        # Add the non-alphabetical characters back to where they were
        for i in non_alpha:
            index = i[0]
            char = i[1]
            pt = ''.join(pt[:index]+char+pt[index:])  
        print(pt)

if __name__ == "__main__":
    main()