using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Xml.Schema;
using ExcelDataReader;

namespace CompiladorChipotludo
{
    public partial class Index : Form
    {
        List<Token> TKList = new List<Token>();
        DataTable Lexic = new DataTable("Palabras");
        int indice;
        public Index()
        {
            InitializeComponent();
            ReadExcel(@"C:\Users\theba\Dictionary.xls");

            Lexic.Columns.Add("Palabra", typeof(string));
            Lexic.Columns.Add("Tipo", typeof(string));
            Lexic.Columns.Add("Longitud", typeof(int));

            richTextBoxWriteZone.Multiline = true;
            richTextBoxWriteZone.AcceptsTab = true;
        }

        private void ReadExcel(string filePath)
        {
            Token tk = new Token();
            string word, type, color;
            using (var stream = File.Open(filePath, FileMode.Open, FileAccess.Read))
            {
                using (var reader = ExcelReaderFactory.CreateReader(stream))
                {

                    var result = reader.AsDataSet();
                    var tables = result.Tables.Cast<DataTable>();

                    foreach (DataTable table in tables)
                    {
                        //LEER LA HOJA PRODUCTOS
                        if (table.TableName == "TOKENS")
                        {
                            table.AcceptChanges();

                            for (int i = 0; i < table.Rows.Count; i++)
                            {
                                tk = new Token();
                                word = table.Rows[i][0].ToString();
                                type = table.Rows[i][1].ToString();
                                color = table.Rows[i][2].ToString();
                                tk.Word = word;
                                tk.Type = type;
                                tk.Color = color;
                                TKList.Add(tk);
                            }
                        }
                    }
                }
            }

        }

        private void button1_Click(object sender, EventArgs e)
        {
            Lexic.Clear();
            string text = richTextBoxWriteZone.Text;
            string coden = text.Replace('\n', ' '); // Reemplazo del caractér "\n" por " "
            string code = coden.Replace('\t', ' ');
            string palabra = "";

            for (int i = 0; i < code.Count(); i++) // Recorrerá cada caratér del código ingresado por el usuario
            {
                if (code[i] != ' ') // Mientras no encuentre espacios en el caracter analizado se agregará a la variable palabra, ejemplo: palabra = hol, code[i] = a, palabra = hola 
                {
                    palabra = palabra + "" + code[i]; // Concatenación de palabra y code[i]
                }
                else // Si detecta un espacio
                {
                    indice = i;
                    palabra = palabra.ToUpper(); // Palabra será convertida a mayusculas

                    for (int j = 0; j < TKList.Count(); j++) // Recorre la lista de Tokens
                    {
                        if(palabra == TKList[j].Word) // Si palabra coincide con un elemento de la lista
                        {
                            Lexic.Rows.Add(TKList[j].Word, TKList[j].Type, TKList[j].Word.Count()); // Se agrega a la palabra Lexic
                        }
                    }

                    palabra = "";
                }                
            }

            if(palabra.Count() > 0) //Al acabar el ciclo y no se detecta un espacio evaluará si palabra tiene alguna "palabra" y hará lo mismo
            {
                palabra = palabra.ToUpper();

                for (int j = 0; j < TKList.Count(); j++)
                {
                    if (palabra == TKList[j].Word)
                    {
                        Lexic.Rows.Add(TKList[j].Word, TKList[j].Type, TKList[j].Word.Count());
                    }
                }
            }

            dataGridView1.DataSource = Lexic;
        }
    }
}
