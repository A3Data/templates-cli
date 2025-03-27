
export type QuestionString = {
    type: "string";
    question: string;
    option: string
    answer: string;
}
export type QuestionBool = {
    type: "bool";
    question: string;
    option: string
    answer: boolean;
}

export type Question = QuestionString | QuestionBool;

export type Template = {
    name: string;
    description: string;
    version: string;
    nixName: string;
    questions: Question[]
}
