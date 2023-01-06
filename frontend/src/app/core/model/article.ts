export interface Article {
    article_id: number
    url: string
    website: string
    published_at: Date
    title: string
    author: string
    subtitle: string
    text: string
    created_at: Date
}

export interface Articles {
    articles: Article[]
}