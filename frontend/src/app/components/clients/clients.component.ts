import { Component, OnInit } from '@angular/core';
import { Client } from 'src/app/core/model/client';
import { CommandService } from 'src/app/core/services/command-service/command.service';

@Component({
  selector: 'app-clients',
  templateUrl: './clients.component.html',
  styleUrls: ['./clients.component.css']
})
export class ClientsComponent implements OnInit {
  constructor(private commandService: CommandService) { }

  clients: Client[] = [];

  ngOnInit() {
    this.getAllClients();
  }

  getAllClients() {
    this.commandService.getAllClients().subscribe({
      next: x => {
        console.log('Observer got a next value: ');
        // console.log(clients);
        this.clients = x.clients;
      },
      error: err => console.error('Observer got an error: ' + err),
      complete: () => console.log('Observer got a complete notification')
    });
  }
  
}
