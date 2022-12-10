import { Component, OnInit } from '@angular/core';
import { Constants } from 'src/app/core/model/constants';
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
  last_dates = {}
  websites_const = Constants.WEBSITES

  ngOnInit(): void {
    console.log('init')
    // var websites = this.getWebsites()
    // console.log(websites)
    this.getAllWebsites()
    this.getAllDelays()
    this.getLastScrapedDates()
  }

  crawl(website: string) {
    console.log("crawl")

    this.commandService.crawl(website).subscribe({
      next: x => {
        console.log('Observer got a next value: ')
        console.log(x)
      },
      error: err => console.error('Observer got an error: ' + err),
      complete: () => console.log('Observer got a complete notification')
    })
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

  getLastScrapedDates() {
    this.commandService.getAllScrapingStarts().subscribe({
      next: x => {
        console.log('Observer got a next value: ')
        console.log(x)
        this.last_dates = x
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
