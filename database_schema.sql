create table document(
    document_id int NOT NULL AUTO_INCREMENT,
    `type` varchar(255) default null,
    reciept varchar(255) default null,
    reciept_date datetime default null,
    PRIMARY KEY (document_id)
);

create table draft(
    draft_id int NOT NULL AUTO_INCREMENT,
    content text default null,
    user varchar(255) default null,
    document_id int NOT NULL,
    PRIMARY KEY (draft_id),
    FOREIGN KEY (document_id) REFERENCES document(document_id)
);

create table copies(
    copy_id int NOT NULL AUTO_INCREMENT,
    `from` varchar(255) not null,
    `to` varchar(255) not null,
    draft_id int,
    PRIMARY KEY (copy_id),
    FOREIGN KEY (draft_id) REFERENCES draft(draft_id)
);