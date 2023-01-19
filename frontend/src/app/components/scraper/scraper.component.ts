import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { NgControl } from '@angular/forms';
import { from } from 'rxjs';
import { Constants } from 'src/app/core/model/constants';
import { ScraperService } from 'src/app/core/services/scraper-service/scraper.service';

@Component({
  selector: 'app-scraper',
  templateUrl: './scraper.component.html',
  styleUrls: ['./scraper.component.scss']
})
export class ScraperComponent implements OnInit {
  constructor(private scraperService: ScraperService) { }

  old_delays: { [key: string]: number } = {}
  old_last_dates: { [key: string]: string } = {}

  delays: { [key: string]: number } = {}
  last_dates: { [key: string]: string } = {}
  websites = Constants.WEBSITES

  @ViewChild('input1') countInput!: ElementRef;
  @ViewChild('input2') timeInput!: ElementRef;
  @ViewChild('input3') dueTimeInput!: ElementRef;

  ngOnInit(): void {
    this.getAllDelays()
    this.getLastScrapedDates()
  }

  crawlOnce(website: string) {
    console.log(`crawlOnce ${website}`)

    this.scraperService.crawlMultipleTimes(website, 1).subscribe({
      next: x => {
        console.log('Observer got a next value: ')
        console.log(x)
        alert(`Pomyślnie uruchomiono scraper na portalu ${website}.`)
      },
      error: err => {
        console.error('Observer got an error: ' + err),
        alert(`Nieznany błąd serwera.`)
      },
      complete: () => console.log('Observer got a complete notification')
    })
  }

  crawlAllMultipleTimes() {
    let crawlsCount = this.countInput.nativeElement.value;
    if (!crawlsCount) {
      alert('Wymagane jest podanie liczby uruchomień.');
      return;
    }
    console.log(`crawlAllMultipleTimes ${crawlsCount}`)

    this.scraperService.crawlAllMultipleTimes(crawlsCount).subscribe({
      next: x => {
        console.log('Observer got a next value: ');
        console.log(x);
        alert(`Uruchomiono scraper dla każdej witryny po ${crawlsCount} razy`);
      },
      error: err => console.error('Observer got an error: ' + err),
      complete: () => console.log('Observer got a complete notification')
    })
  }

  crawlAllForGivenTime() {
    let runTime = this.timeInput.nativeElement.value;
    if (!runTime) {
      alert('Wymagane jest podanie liczby sekund uruchomienia scrapera.')
      return;
    }
    console.log(`crawlAllForGivenTime ${runTime}`)

    this.scraperService.crawlAllForGivenTime(runTime).subscribe({
      next: x => {
        console.log('Observer got a next value: ')
        console.log(x)
        alert(`Uruchomiono scraper dla każdej witryny na ${runTime} sekund`);
      },
      error: err => console.error('Observer got an error: ' + err),
      complete: () => console.log('Observer got a complete notification')
    })
  }

  crawlAllToDueTime() {
    let dueTime = this.dueTimeInput.nativeElement.value;

    if (!dueTime) {
      alert('Wymagane jest podanie daty zakończenia działania scrapera.')
      return;
    }
    console.log(`crawlAllToDueTime ${dueTime}`)

    // to ISO format
    let date = new Date(dueTime);
    let dueTimeUTC= date.toISOString()

    this.scraperService.crawlAllToDueTime(dueTimeUTC).subscribe({
      next: x => {
        console.log('Observer got a next value: ')
        console.log(x)
        alert(`Uruchomiono scraper dla każdej witryny do daty zakończenia: ${dueTime}`);
      },
      error: err => console.error('Observer got an error: ' + err),
      complete: () => console.log('Observer got a complete notification')
    })
  }

  getAllDelays() {
    this.scraperService.getAllDelays().subscribe({
      next: x => {
        console.log('Observer got a next value: ');
        console.log(x);
        this.delays = x;
        this.old_delays = {...this.delays};
      },
      error: err => console.error('Observer got an error: ' + err),
      complete: () => console.log('Observer got a complete notification')
    })
  }

  getLastScrapedDates() {
    this.scraperService.getAllScrapingStarts().subscribe({
      next: x => {
        console.log('Observer got a next value: ');
        console.log(x);
        this.last_dates = x;
        // for (var key in this.last_dates) {
        //   this.last_dates[key] = new Date(this.last_dates[key]);
        // }
        this.old_last_dates = {...this.last_dates};
      },
      error: err => console.error('Observer got an error: ' + err),
      complete: () => console.log('Observer got a complete notification')
    })
  }

  setDelays() {
    for (var website in this.delays) {
      if (this.delays[website] != this.old_delays[website]) {
        let delay = this.delays[website];
        this.scraperService.setDelay(website, delay).subscribe({
          next: x => {
            console.log('Observer got a next value: ');
            console.log(x);
          },
          error: err => console.error('Observer got an error: ' + err),
          complete: () => {
            console.log('Observer got a complete notification');
            this.getAllDelays();
          }
        });
      }
    };
  }

  setLastScrapedDates() {
    for (var website in this.last_dates) {
      if (this.last_dates[website] != this.old_last_dates[website]) {
        let date = this.last_dates[website];
        this.scraperService.setScrapingStart(website, date).subscribe({
          next: x => {
            console.log('Observer got a next value: ');
            console.log(x);
          },
          error: err => console.error('Observer got an error: ' + err),
          complete: () => {
            console.log('Observer got a complete notification');
            this.getLastScrapedDates();
          }
        });
      }
    };
  }

  hasDelaysChanged() {
    for (var key in this.delays) {
      if (this.delays[key] != this.old_delays[key]) {
        return true;
      }
    }
    return false;
  }

  hasLastDatesChanged() {
    for (var key in this.last_dates) {
      if (this.last_dates[key] != this.old_last_dates[key]) {
        return true;
      }
    }
    return false;
  }

  hasSettingsChanged() {
    return this.hasDelaysChanged() || this.hasLastDatesChanged();
  }

  onSubmit() {
    this.setDelays();
    this.setLastScrapedDates();
    // var isDelayUpdated = false;
    // for (var key in this.delays) {
    //   if (this.delays[key] != this.old_delays[key]) {
    //     isDelayUpdated = true;
    //     break;
    //   }
    // }

    // var isLastDateUpdated = false;
    // for (var key in this.last_dates) {
    //   if (this.last_dates[key] != this.old_last_dates[key]) {
    //     isLastDateUpdated = true;
    //     break;
    //   }
    // }

    // if (!isDelayUpdated && !isLastDateUpdated) {
    //   alert('Brak zmian.');
    // }
    // else {
    //   alert('Aktualizowanie ustawień.');
    //   if (isDelayUpdated) {
    //     this.setDelays();
    //   }
    //   if (isLastDateUpdated) {
    //     this.setLastScrapedDates();
    //   }
    // }
  }

  // trackByIndex(index: number, obj: any): any {
  //   return index;
  // }
}
