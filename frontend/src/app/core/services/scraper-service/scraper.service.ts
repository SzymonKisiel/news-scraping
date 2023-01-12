import { Inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http'
import { Constants } from '../../model/constants';
import { API_URL } from '../../tokens';

@Injectable({
  providedIn: 'root'
})
export class ScraperService {

  constructor(
    @Inject(API_URL) private apiUrl: string,
    private httpClient: HttpClient) { }

  apiPath = '/api/command-handler/'
  
  _crawl(body: { [key: string] : any}) {
    const action = 'crawl';
    const url = this.apiUrl + this.apiPath + action;

    return this.httpClient.post(url, body)
  }

  crawlMultipleTimes(website: string, crawlsAmount: number) {
    const body = {
      "websites": [
        website
      ],
      "crawls_amount": crawlsAmount
    };
    return this._crawl(body);
  }

  crawlAllMultipleTimes(crawlsAmount: number) {
    const body = {
      "websites": Constants.WEBSITES,
      "crawls_amount": crawlsAmount
    };
    return this._crawl(body);
  }

  crawlToDueTime(website: string, dueTime: Date) {
    const body = {
      "websites": [
        website
      ],
      "due_time": dueTime.toISOString()
    };
    return this._crawl(body);
  }

  crawlAllToDueTime(dueTime: string) {
    const body = {
      "websites": Constants.WEBSITES,
      "due_time": dueTime
    };
    return this._crawl(body);
  }

  crawlForGivenTime(website: string, runTime: number) {
    const body = {
      "websites": [
        website
      ],
      "run_time": runTime
    };
    return this._crawl(body);
  }

  crawlAllForGivenTime(runTime: number) {
    const body = {
      "websites": Constants.WEBSITES,
      "run_time": runTime
    };
    return this._crawl(body);
  }
  
  getAllDelays() {
    const action = 'get-delay'
    const url = this.apiUrl + this.apiPath + action
    const body = {
      "websites": Constants.WEBSITES
    }
    return this.httpClient.post<any>(url, body)
  }
  
  getAllScrapingStarts() {
    const action = 'get-scraping-start'
    const url = this.apiUrl + this.apiPath + action
    const body = {
      "websites": Constants.WEBSITES
    }
    return this.httpClient.post<any>(url, body)
  }
  
  getWebsites() {
    const action = 'get-websites'
    const url = this.apiUrl + this.apiPath + action
    return this.httpClient.get(url) 
  }

  setDelay(website: string, delay: number) {
    console.log(`setDelay: ${website} ${delay}`);
    const action = 'set-delay';
    const url = this.apiUrl + this.apiPath + action;
    const body = {
      "websites": [
        website
      ],
      "delay": delay
    }

    return this.httpClient.post(url, body);
  }

  setScrapingStart(website: string, lastScrapedDate: string) {
    // console.log(`setDelay: ${website} ${lastScrapedDate.toISOString()}`);
    const action = 'set-scraping-start';
    const url = this.apiUrl + this.apiPath + action;
    const body = {
      "websites": [
        website
      ],
      "date": lastScrapedDate
      // "date": lastScrapedDate.toISOString()
    }

    return this.httpClient.post(url, body);
  }
}
