# csharp

## Advanced stuff

### `Task`, `async`, `await`, Event handlers

:material-warning: TBD

* A synchronous job using `Thread.Sleep()` to wait for 5 seconds before completion (execution time: ~5030ms):

```csharp
using System;
using System.Collections.Generic;
using System.IO;
using System.Threading.Tasks;
using System.Runtime.CompilerServices;

namespace Kitchen
{
    class Program
    {
        static async Task Main(string[] args)
        {
            Program program = new Program();
            program.MakeFoodSync("Lentils soup");
        }

        public void MakeFoodSync(string foodItem)
        {
            // start timer
            var watch = System.Diagnostics.Stopwatch.StartNew();

            Console.WriteLine($"Preparing {foodItem}...");
            Thread.Sleep(5000); // <---- Notice the Thread namespace
            Console.WriteLine($"{foodItem} is ready!");

            // stop timer
            watch.Stop();
            Console.WriteLine("Elapsed : " + watch.ElapsedMilliseconds);
        }
    }
}
```

* An asynchronous job using `await Task.Delay()` (execution time: ~5030ms)

```csharp
using System;
using System.Collections.Generic;
using System.IO;
using System.Threading.Tasks;
using System.Runtime.CompilerServices;

namespace Kitchen
{
    class Program
    {
        static async Task Main(string[] args)
        {
            Program program = new Program();
            await program.MakeFoodAsync("Lentils soup");
        }

        public async Task MakeFoodAsync(string foodItem)
        {
            // start timer
            var watch = System.Diagnostics.Stopwatch.StartNew();

            Console.WriteLine($"Preparing {foodItem}...");
            await Task.Delay(5000);
            Console.WriteLine($"{foodItem} is ready!");

            // stop timer
            watch.Stop();
            Console.WriteLine("Elapsed : " + watch.ElapsedMilliseconds);
        }
    }
}
```



### `yield return`

:material-warning: TBD

https://exercism.org/tracks/csharp/exercises/accumulate

```csharp
using System;
using System.Collections.Generic;
using System.Linq;
using System.IO;

public class Program
{

    // Initial array
    var array = new[] { "A", "B", "C", "D"};

    public static void Main()
    {
        // Calling Test()
    }

    // Interface for enumerable objects
    // Used by: Lists, Arrays, Dictionaries, etc.
    public IEnumerable<string> Test() {
      
      // Con ToList l'oggetto array viene processato _tutto insieme_
      // Quindi viene allocata memoria per l'oggetto nella sua interezza:
      // return array.ToList();

      // Altra maniera "manuale" di allocare tutto l'oggetto enumerabile
      // Usando una lista 'temp' da riempire man mano
      var temp = New List<string>();
      foreach (var item in array){
        temp.Add(item);
      }
      return temp;

      // In questa modalità, invece, il return non chiude la funzione
      // Bensì all'oggetto chiamante ritorna man mano il risultato
      // dell'iterazione
      foreach (var item in array)
      {
        yield return item;
      }

      // Esempio classico: lettura di un file di grandi dimensioni
      // Qui sotto alloco il contenuto del file nella sua interezza
      var file = File.OpenRead("filePath.txt");
      // Qui invece leggo ed elaboro una riga alla volta
      using (var sr = new StreamReader(File.OpenRead("filePath.txt")))
      {
        while (!sr.EndOfStream){

            var line = sr.ReadLine();
            
            // Se si volesse fermare l'iterazione in corrispondenza
            // di una determinata condizione (es. riga vuota):
            // if (line.IsEmpty)
            //      yield break;

            yield return line;
        }
      }
    }

    // Vari modi per consumare un enumerable
    public void TestConsumeEnumerable() {
      var enumerable = Test();

      // ToArray: un modo di consumare un enumerable
      var values = enumerable.ToArray();

      // Enumerator: altro modo di consumare un enumerable
      var enumerator = enumerable.GetEnumerator();
      while (enumerator.MoveNext())
      {
        var item = enumerator.Current;
      }
    }

}
```

#### `IAsyncEnumerable`

Same as before with `IAsyncEnumerable`:

```csharp
using System;
using System.Collections.Generic;
using System.Linq;

public class Program
{
  var array = new[] {"A", "B", "C", "D"};

  public static void Main()
  {
    // Calling Test()
  }

  public async Task TestConsumeEnumerable(){
    var enumerable = Test();
    await foreach (var item in enumerable)
    {
      Console.WriteLine(item);
      // Save on database
      // ...
    }
  }

  public async IAsyncEnumerable<string> Test()
  {
    using (var sr = new StreamReader(File.OpenRead("filePath.txt")))
    {
        while (!sr.EndOfStream){
            var line = await sr.ReadLineAsync();
            yield return line;
        }
    }
  }
}
```

### Nested Types

:material-warning: TBD

> [:material-stack-overflow: cannot reference a type through an expression](https://stackoverflow.com/questions/33616006/generalinformation-cannot-reference-a-type-through-an-expression-try-webquo)
> [:material-stack-overflow: calling the nested class from the parent class](https://stackoverflow.com/questions/2549413/nested-class-calling-the-nested-class-from-the-parent-class)

```csharp
// Outer class
public class OuterClass
{
    // Property
    public string OuterClassProperty { get; set; }
    private Speed currentSpeed;

    // inner class
    public class InnerClass {

        // Instance of the parent class passed to the inner class' constructor
        // So that you can call outer's methods from inside inner
        private OuterClass _parentCar;
        public InnerClass(OuterClass parentCar){
            _parentCar = parentCar;
        }

        public void ShowSponsor(string sponsorName) {
            _parentCar.SetSponsor(sponsorName);
        }
    
        public void Calibrate(){
        }

        public bool SelfTest() => true;
 
        public void SetSpeed(decimal amount, string unitsString){
            SpeedUnits speedUnits = SpeedUnits.MetersPerSecond;
            if (unitsString == "cps")
                speedUnits = SpeedUnits.CentimetersPerSecond;
            _parentCar.SetSpeed(new Speed(amount, speedUnits));
        }
        
    }

    // Properties
    public InnerClass Telemetry { get; set; }
    public Speed CarSpeed { get; set; }

    // Constructor with nested classes
    public OuterClass() {
        Telemetry = new InnerClass(this);
        CarSpeed = new Speed(0, SpeedUnits.MetersPerSecond);
    }
    
    public string GetSpeed() => currentSpeed.ToString();

    private void SetSponsor(string sponsorName)
    {
        OuterClassProperty = sponsorName;
    }

    private void SetSpeed(Speed speed)
    {
        currentSpeed = speed;
    }
}
```

### Operator overloading

:material-warning: TBD

https://exercism.org/tracks/csharp/exercises/hyperia-forex

### Reflection methods

#### Get the list of properties of an object in order of declaration

```csharp
    // https://stackoverflow.com/questions/9062235/get-properties-in-order-of-declaration-using-reflection
    var properties = typeof(YOUR_TYPE_HERE)
      .GetProperties(BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic)
      .OrderBy(x => x.MetadataToken);
    
    // just printing
    foreach(var property in properties){ Console.WriteLine(property.Name); }
```