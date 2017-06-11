//Import statements
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;
import java.util.Scanner;
import java.io.File;

public class PhoneDict
{

   public static void main (String args[]) throws IOException
   {
       //Main variables
       String input_code;
       Map<String, ArrayList<String>> word_to_code = new HashMap<String, ArrayList<String>>();
       ArrayList<String> indexed_code = new ArrayList<String>();
       String cur_code = "";
       String final_output = "";
       /*
       ArrayList<String> value_at_key = new ArrayList<String>();
       String word_option  = "";
       boolean first_real_num = false;
       */


       //The name of the file that contains the words
       //String ACMIA_WORDS = "word_list";

       //IMPORTANT
       String file_words = System.getenv("ACMIA_WORDS");
		  File file_obj = new File(file_words);

       //Stores the words from the text file speicified by String ACMIA_WORDS in the Scanner words
       Scanner words = new Scanner( new FileReader( file_obj )) ;

       //Stores the user input code in the Scanner input_code
       Scanner user_input = new Scanner (System.in);

       //Making the Map word_to_code
       word_to_code = make_map(words);

       //System.out.println(word_to_code);


       //Runs infinitely
       while(true)
       {
           //Getting the input code from the user
           input_code = user_input.nextLine();

           //Parsing the input code
           String parsed_code = parse_input_code(input_code);

           //System.out.println(parsed_code);

           //Going through each character of the parsed code
           for (int i = 0; i < parsed_code.length(); i++)
           {
               //If the current character is a digit, then it is part of a word
               if(Character.isDigit(parsed_code.charAt(i)))
               {
                   //Formulating a String for each word based on its text code
                   cur_code += parsed_code.charAt(i);
               }
               //Otherwise, it is a space character
               else
               {
                   //Adding the current code to the ArrayList indexed_code
                   indexed_code.add(cur_code);
                   cur_code = "";
               }
           }

           //System.out.println(indexed_code);

           //Getting the final output, sending the Map word_to_code and the ArrayList indexed_code to complete this task
           final_output = create_final_output(word_to_code, indexed_code);

           //Printing the final output
           System.out.println(final_output);

           //Clearing the ArrayList of the indexed code
           indexed_code.clear();
       }

   }

















   public static Map<String, ArrayList<String>> make_map (Scanner w)
   {
       //Function variables
       String cur_word;
       String word_code;
       Map<String, ArrayList<String>> word_to_code = new HashMap<String, ArrayList<String>>();


       //While there is more in the file
       while (w.hasNext())
       {
           //Getting the next word in the file
           cur_word = w.next();
           //Getting the length of the word
           int cur_word_len = cur_word.length();
           //Producing the text code from the given word
           word_code = make_word_code(cur_word, cur_word_len);

           //If the Map already contains this text code, append the word to the value at the key
           if (word_to_code.containsKey(word_code))
           {
               //Getting the ArrayList value at a specific key
               ArrayList<String> value_at_key = word_to_code.get(word_code);
               //Appending the current word to the ArrayList value
               value_at_key.add(cur_word);
               //Replacing the key's ArrayList value with the newly-expanded ArrayList
               word_to_code.put(word_code, value_at_key);
           }
           //If the Map does not contain the text code, make a new key and value entry in the Map
           else
           {
               //An ArrayList for the new value at the key
               ArrayList<String> new_value = new ArrayList<String>();
               //Adding the current word to the ArrayList
               new_value.add(cur_word);
               //Adding the ArrayList value to the key
               word_to_code.put(word_code, new_value);
           }

           //Erasing the content of the String word_code
           word_code = "";
       }

       //Returning the word_to_code Map
       return word_to_code;
   }

   public static String make_word_code (String w, int l)
   {
       //String word_code
       String word_code = "";

       //Going through each character of the String w
       for (int i = 0; i < l; i++)
       {
           //Getting the current letter of the String w
           char cur_letter = w.charAt(i);
           //Making the letter uppercase
           cur_letter = Character.toUpperCase(cur_letter);
           //Determining the letter's corresponding text code number
           word_code += letter_to_num(cur_letter);
       }

       //Returning the word code
       return(word_code);
   }

   public static String letter_to_num (char l)
   {
       //String word_code
       String word_code = "";

       //Going through each character and determining its corresponding text code number
       switch (l)
       {
           case 'A':
           case 'B':
           case 'C':
           {
               word_code += "2";
               break;
           }
           case 'D':
           case 'E':
           case 'F':
           {
               word_code += "3";
               break;
           }
           case 'G':
           case 'H':
           case 'I':
           {
               word_code += "4";
               break;
           }
           case 'J':
           case 'K':
           case 'L':
           {
               word_code += "5";
               break;
           }
           case 'M':
           case 'N':
           case 'O':
           {
               word_code += "6";
               break;
           }
           case 'P':
           case 'Q':
           case 'R':
           case 'S':
           {
               word_code += "7";
               break;
           }
           case 'T':
           case 'U':
           case 'V':
           {
               word_code += "8";
               break;
           }
           case 'W':
           case 'X':
           case 'Y':
           case 'Z':
           {
               word_code += "9";
               break;
           }
       }

       //Returning the total word code
       return word_code;
   }

   public static String parse_input_code (String ic)
   {
       //Function variables
       boolean first_real_num = false;
       boolean first_zero = true;
       String word_choices = "";
       String parse_code = "";
       boolean hasNonZero = false;

       //Making it so that if only zeroes are entered, they are treated as a blank line
       if (ic.length() != 0)
       {
           //Going through each character of ic
           for (int i = 0; i < ic.length(); i++)
           {
               //If all of ic contains some non-zero character, then the String does have non-zero values
               if(ic.charAt(i) != '0')
               {
                   hasNonZero = true;
               }
           }
       }

       //If a blank line is entered, then a blank line is returned
       if (ic.length() == 0 || hasNonZero == false)
       {
           parse_code = "";
       }
       //If the input is not a blank line
       else
       {
           //Going through each index of the String ic
           for (int i = 0; i < ic.length(); i++)
           {
               //Getting the character at the current index of String ic
               char cur_num = ic.charAt(i);

               //If the current number is a 0 and we have not hit a non-zero number...
               if( cur_num == '0' && first_real_num == false)
               {
                   //do nothing
               }
               //If the current number is not a 0 and it is the first non-zero number...
               else
               {
                   //Set first_real_num = true
                   first_real_num = true;
               }

               //If we have already hit the first non-zero number...
               if(first_real_num == true) {
                   //If the current number is a zero...
                   if (cur_num == '0') {
                       //If i = length - 1, then the last character is a zero
                       if (i == ic.length() - 1) {
                           //Because it's the LAST zero, first_zero = false (do not add a space to the end)
                           first_zero = false;
                       }

                       //If the current zero is the first zero in a sequence (of zeroes or non-zero numbers)...
                       if (first_zero == true) {
                           //Add an underscore to the parsed code (delimiter)
                           parse_code += "_";
                           //Set first_zero to equal false, thus ignoring the other zeroes in the sequence after the current zero (if more zeroes follow the current zero)
                           first_zero = false;
                       }

                   }
                   //If the current number is not a zero...
                   else {
                       //Add the current number to the parsed code
                       parse_code += cur_num;
                       //Set first_zero = true, since the next zero to appear will be the first zero in its sequence (given that the current number is not a zero)
                       first_zero = true;
                   }
               }

           }

           //Removing a trailing underscore from the String parse_code, if it exists
       /*if( parse_code.charAt(parse_code.length()-1) == '_' )
       {
           StringBuilder sb = new StringBuilder(parse_code);
           sb.deleteCharAt(parse_code.length()-1);
           parse_code=sb.toString();
       }*/

           //Ensuring that the parsed code ends with an underscore
           if( parse_code.charAt(parse_code.length()-1) != '_')
           {
               parse_code += "_";
           }
       }



       //returning the parsed code
       return parse_code;

   }

   public static String create_final_output (Map<String, ArrayList<String>> m, ArrayList<String> l)
   {
       //Function variables
       ArrayList<String> value_at_key = new ArrayList<String>();
       String final_output = "";
       String word_option  = "";
       boolean first_real_num = false;

       //Going through each index of the ArrayList l
       for(int i = 0; i < l.size(); i++)
       {
           //If the Map m contains the key given byt he current index of l
           if(m.containsKey(l.get(i)))
           {
               //Get the ArrayList value at that key
               value_at_key = m.get(l.get(i));

               //If the ArrayList only contains one element, output that element
               if(value_at_key.size() == 1)
               {
                   final_output += value_at_key.get(0) + " ";
               }
               //If the ArrayList contains multiple elements, output all elements concatenated
               else
               {
                   //Starting the concatenationf of the words with a parenthesis
                   word_option = "(";
                   //Going through each element of the ArrayList
                   for (int j = 0; j < value_at_key.size(); j++)
                   {
                       //If we are at the end of the ArrayList, get the last word and append the ending parenthesis to the String word_option
                       if (j == value_at_key.size() - 1)
                       {
                           word_option += value_at_key.get(j);
                           word_option += ")";
                       }
                       //If we are not at the end of the ArrayList, get the current word and append a line, thus separating each word
                       else
                       {
                           word_option += value_at_key.get(j);
                           word_option += "|";
                       }
                   }

                   //Adding the String word_option to the String final_output, separated by a space
                   final_output += word_option + " ";

                   //Clearing the String word_option
                   word_option = "";
               }

           }
           //If the Map m does not contain the key given by the current index of l, produce a pseudo-word
           else
           {
               //Indexing through the size of the word
               for (int j = 0; j < l.get(i).length(); j++)
               {
                   // can't find word in the Map m, put stars that are the same length as the inputted word
                   word_option += "*";
               }

               //Adding the pseudo-word to the String final_output
               final_output += word_option + " ";

               //Clearing the String word_option
               word_option = "";
           }
       }

       //Returning the String final_output
       return final_output;
   }

}