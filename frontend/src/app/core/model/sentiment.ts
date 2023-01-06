import { Article } from "./article";
import { SearchTerm } from "./search_term";

export interface Sentiment {
    id: number,

    article_id: number,
    article: Article,

    search_term_id: number,
    search_term: SearchTerm,

    sentence: string,
    positive_score: number,
    neutral_score: number,
    negative_score: number,
    overall_sentiment: number
}

export interface Sentiments {
    sentiments: Sentiment[]
}