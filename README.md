# CompressionAlgorithm

Compressing text files via telegram bot.  

[**compression**](https://github.com/alyabogd/CompressionAlgorithm/tree/master/compression) package contains a clear 
implementation of the _arithmetic compression algorithm_.   
The high idea is to encode the entire message into a single number in range _0 <= p <= 1_. 
The efficiency of the algorithm on random Russian novels is about 35-40%. Read more [here](https://en.wikipedia.org/wiki/Arithmetic_coding). 

Feel free to use scripts to compress or decompress your files from the command line.

Example:

    `compress.py InFile CompressedFile`
  
    `decompress.py CompressedFile OutFile`


You can also use telegram bot, which has some other useful features such as compressing all text files found on a given web-page.
Start a dialog with *@arithmetic_compressor_bot* and follow further instructions.
