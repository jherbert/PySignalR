using System;
using System.Threading.Tasks;
using Microsoft.AspNetCore.SignalR.Client;

namespace CSharp
{
    class Program
    {
        static async Task Main(string[] args)
        {
            var exitEvent = false;
            Console.CancelKeyPress += (sender, eventArgs) =>
            {
                eventArgs.Cancel = true;
                exitEvent = true;
            };
            var clientName = ".NET Client";

            var connection = new HubConnectionBuilder()
                .WithUrl("http://localhost:5000/chatHub")
                .Build();

            connection.On<string, string>("ReceiveMessage", (user, message) =>
            {
                Console.WriteLine("{0} says: {1}", user, message);
            });

            connection.On<string>("ClientConnected", (message) =>
            {
                Console.WriteLine(">> {0}", message);
            });
            

            connection.Closed += async (error) =>
            {
                await Task.Delay(new Random().Next(0, 5) * 1000);
                await connection.StartAsync();
            };

            await connection.StartAsync();

            while (!exitEvent)
            {
                Console.Write("> ");
                var message = Console.ReadLine();

                if (!string.IsNullOrEmpty(message))
                {
                    await connection.InvokeAsync("SendMessage", clientName, message);
                }
            }

            await connection.StopAsync();
        }
    }
}
