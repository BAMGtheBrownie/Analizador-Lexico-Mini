using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace CompiladorChipotludo
{
    public class Token
    {
        string word, type, color;

        public Token(string word, string type, string color) 
        { 
            this.word = word;
            this.type = type;
            this.color = color;
        }

        public Token()
        {
            this.word = "";
            this.type = "";
            this.color = "";
        }

        public string Word
        { 
            get { return word; }
            set { word = value; }
        }

        public string Type
        {
            get { return type; }
            set { type = value; }
        }

        public string Color
        {
            get { return color; }
            set { color = value; }
        }
    }
}
