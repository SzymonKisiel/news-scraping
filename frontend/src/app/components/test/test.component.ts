import { Component, OnInit } from '@angular/core';
import { CommandService } from 'src/app/core/services/command-service/command.service';

@Component({
  selector: 'app-test',
  templateUrl: './test.component.html',
  styleUrls: ['./test.component.css']
})
export class TestComponent implements OnInit {
  constructor(private commandService: CommandService) { }

  delays = {}
  websites = {}

  ngOnInit(): void {
    console.log('init')
    // var websites = this.getWebsites()
    // console.log(websites)
    this.getAllWebsites()
    this.getAllDelays()
  }

  getAllDelays() {
    this.commandService.getAllDelays().subscribe({
      next: x => {
        console.log('Observer got a next value: ')
        console.log(x)
        this.delays = x
      },
      error: err => console.error('Observer got an error: ' + err),
      complete: () => console.log('Observer got a complete notification')
    })
  }

  getAllWebsites() {
    this.commandService.getWebsites().subscribe({
      next: x => {
        console.log('Observer got a next value: ')
        console.log(x)
        this.websites = x
      },
      error: err => console.error('Observer got an error: ' + err),
      complete: () => console.log('Observer got a complete notification')
    })
  }
}
