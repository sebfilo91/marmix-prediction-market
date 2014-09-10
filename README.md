marmix-prediction-market
========================



========================


Deployment SQL Script : 


CREATE TABLE UserAction (
  id                    SERIAL NOT NULL, 
  "date"               date NOT NULL, 
  device_type          varchar(4) NOT NULL, 
  type                 varchar(4) NOT NULL, 
  NUM_USER_ACTION_USER int4 NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE Trader (
  id                   SERIAL NOT NULL, 
  address1            varchar(255) NOT NULL, 
  address2            varchar(255), 
  zipcode             varchar(10) NOT NULL, 
  country             varchar(255) NOT NULL, 
  city                varchar(255) NOT NULL, 
  countrystate        varchar(255), 
  birthdate           timestamp, 
  cash                numeric(15, 6) NOT NULL, 
  NUM_TRADER_USER     int4 NOT NULL, 
  NUM_TRADER_CURRENCY int4 NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE MarketTransaction (
  id                        SERIAL NOT NULL, 
  quantity                 int4 NOT NULL, 
  price                    numeric(15, 6) NOT NULL, 
  result                   numeric(15, 6) NOT NULL, 
  "date"                   timestamp NOT NULL, 
  NUM_TRANSACTION_TRADER   int4 NOT NULL, 
  NUM_TRANSACTION_CURRENCY int4 NOT NULL, 
  NUM_TRANSACTION_ORDER    int4 NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE Alert (
  id                SERIAL NOT NULL, 
  price            numeric(15, 6) NOT NULL, 
  description      varchar(512), 
  NUM_ALERT_CLAIM  int4 NOT NULL, 
  NUM_ALERT_TRADER int4 NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE MarketOrder (
  id                SERIAL NOT NULL, 
  quantity         int4 NOT NULL, 
  min_price        numeric(15, 6), 
  max_price        numeric(15, 6), 
  date_sent        timestamp NOT NULL, 
  date_expire      timestamp NOT NULL, 
  filled           bool NOT NULL, 
  NUM_ORDER_TRADER int4 NOT NULL, 
  NUM_ORDER_CLAIM  int4 NOT NULL, 
  NUM_ORDER_TYPE   int4 NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE Claim (
  id                  SERIAL NOT NULL, 
  name               varchar(1024) NOT NULL UNIQUE, 
  min_value          numeric(15, 6) NOT NULL, 
  max_value          numeric(15, 6) NOT NULL, 
  end_value          numeric(15, 6), 
  price              numeric(15, 6), 
  ticks              numeric(15, 6) NOT NULL, 
  end_date           timestamp, 
  create_date        timestamp NOT NULL, 
  ipo_date           timestamp, 
  description        varchar(255) NOT NULL, 
  success_condition  varchar(255) NOT NULL, 
  special_condition  varchar(255), 
  NUM_CLAIM_CURRENCY int4 NOT NULL, 
  NUM_CLAIM_TYPE     int4 NOT NULL, 
  NUM_CLAIM_STATUS   int4 NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE ClaimHistory (
  id                       SERIAL NOT NULL, 
  "date"                  timestamp NOT NULL, 
  price                   numeric(15, 6) NOT NULL, 
  NUM_CLAIM_HISTORY_CLAIM int4 NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE Reward (
  id                 SERIAL NOT NULL, 
  description       varchar(1024) NOT NULL, 
  "condition"       varchar(1024) NOT NULL, 
  NUM_REWARD_TRADER int4 NOT NULL, 
  NUM_REWARD_TYPE   int4 NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE Configuration (
  id     SERIAL NOT NULL, 
  "key" varchar(255) NOT NULL, 
  value varchar(255) NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE MarketMaker (
  NUM_MARKETMAKER_CLAIM  int4 NOT NULL, 
  NUM_MARKETMAKER_TRADER int4 NOT NULL, 
  quantity               int4 NOT NULL);
CREATE TABLE UserComment (
  id                  SERIAL NOT NULL, 
  text               varchar(1024) NOT NULL, 
  date_update        timestamp, 
  NUM_COMMENT_TRADER int4 NOT NULL, 
  NUM_COMMENT_CLAIM  int4 NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE Help (
  id             SERIAL NOT NULL, 
  page          varchar(255) NOT NULL, 
  html_id       varchar(255) NOT NULL, 
  title         varchar(255) NOT NULL, 
  description   varchar(1024) NOT NULL, 
  NUM_HELP_TYPE int4 NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE Holding (
  id                  SERIAL NOT NULL, 
  quantity           int4 NOT NULL, 
  "date"             timestamp NOT NULL, 
  price              numeric(15, 6) NOT NULL, 
  NUM_HOLDING_CLAIM  int4 NOT NULL, 
  NUM_HOLDING_TRADER int4 NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE Currency (
  id      SERIAL NOT NULL, 
  symbol varchar(3) NOT NULL, 
  name   varchar(100) NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE Exchange (
  id                 SERIAL NOT NULL, 
  "date"            timestamp NOT NULL, 
  rate              numeric(15, 6) NOT NULL, 
  NUM_CURRENCY_SRC  int4 NOT NULL, 
  NUM_CURRENCY_DEST int4 NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE OrderType (
  id    SERIAL NOT NULL, 
  name varchar(50) NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE HelpType (
  id    SERIAL NOT NULL, 
  name varchar(50) NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE ClaimType (
  id    SERIAL NOT NULL, 
  name varchar(50) NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE RewardType (
  id    SERIAL NOT NULL, 
  name varchar(50) NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE ClaimStatus (
  id    SERIAL NOT NULL, 
  name varchar(50) NOT NULL, 
  PRIMARY KEY (id));
  
ALTER TABLE MarketTransaction ADD CONSTRAINT FK_NUM_TRANSACTION_TRADER FOREIGN KEY (NUM_TRANSACTION_TRADER) REFERENCES Trader (id);
ALTER TABLE Trader ADD CONSTRAINT FK_NUM_TRADER_USER FOREIGN KEY (NUM_TRADER_USER) REFERENCES auth_user (id);
ALTER TABLE MarketOrder ADD CONSTRAINT FK_NUM_ORDER_TRADER FOREIGN KEY (NUM_ORDER_TRADER) REFERENCES Trader (id);
ALTER TABLE UserAction ADD CONSTRAINT FK_NUM_USER_ACTION_USER FOREIGN KEY (NUM_USER_ACTION_USER) REFERENCES auth_user (id);
ALTER TABLE ClaimHistory ADD CONSTRAINT FK_NUM_CLAIM_HISTORY_CLAIM FOREIGN KEY (NUM_CLAIM_HISTORY_CLAIM) REFERENCES Claim (id);
ALTER TABLE MarketOrder ADD CONSTRAINT FK_NUM_ORDER_CLAIM FOREIGN KEY (NUM_ORDER_CLAIM) REFERENCES Claim (id);
ALTER TABLE UserComment ADD CONSTRAINT FK_NUM_COMMENT_CLAIM FOREIGN KEY (NUM_COMMENT_CLAIM) REFERENCES Claim (id);
ALTER TABLE UserComment ADD CONSTRAINT FK_NUM_COMMENT_TRADER FOREIGN KEY (NUM_COMMENT_TRADER) REFERENCES Trader (id);
ALTER TABLE Alert ADD CONSTRAINT FK_NUM_ALERT_CLAIM FOREIGN KEY (NUM_ALERT_CLAIM) REFERENCES Claim (id);
ALTER TABLE Marketmaker ADD CONSTRAINT FK_NUM_MARKETMAKER_CLAIM FOREIGN KEY (NUM_MARKETMAKER_CLAIM) REFERENCES Claim (id);
ALTER TABLE Holding ADD CONSTRAINT FK_NUM_HOLDING_CLAIM FOREIGN KEY (NUM_HOLDING_CLAIM) REFERENCES Claim (id);
ALTER TABLE Holding ADD CONSTRAINT FK_NUM_HOLDING_TRADER FOREIGN KEY (NUM_HOLDING_TRADER) REFERENCES Holding (id);
ALTER TABLE Marketmaker ADD CONSTRAINT FK_NUM_MARKETMAKER_TRADER FOREIGN KEY (NUM_MARKETMAKER_TRADER) REFERENCES Trader (id);
ALTER TABLE Trader ADD CONSTRAINT FK_NUM_TRADER_CURRENCY FOREIGN KEY (NUM_TRADER_CURRENCY) REFERENCES Currency (id);
ALTER TABLE MarketTransaction ADD CONSTRAINT FK_NUM_TRANSACTION_CURRENCY FOREIGN KEY (NUM_TRANSACTION_CURRENCY) REFERENCES Currency (id);
ALTER TABLE Alert ADD CONSTRAINT FK_NUM_ALERT_TRADER FOREIGN KEY (NUM_ALERT_TRADER) REFERENCES Trader (id);
ALTER TABLE Claim ADD CONSTRAINT FK_NUM_CLAIM_CURRENCY FOREIGN KEY (NUM_CLAIM_CURRENCY) REFERENCES Currency (id);
ALTER TABLE Reward ADD CONSTRAINT FK_NUM_REWARD_TRADER FOREIGN KEY (NUM_REWARD_TRADER) REFERENCES Trader (id);
ALTER TABLE MarketTransaction ADD CONSTRAINT FK_NUM_TRANSACTION_ORDER FOREIGN KEY (NUM_TRANSACTION_ORDER) REFERENCES MarketOrder (id);
ALTER TABLE Exchange ADD CONSTRAINT FK_NUM_CURRENCY_SRC FOREIGN KEY (NUM_CURRENCY_SRC) REFERENCES Currency (id);
ALTER TABLE Exchange ADD CONSTRAINT FK_NUM_CURRENCY_DEST FOREIGN KEY (NUM_CURRENCY_DEST) REFERENCES Currency (id);
ALTER TABLE MarketOrder ADD CONSTRAINT FK_NUM_ORDER_TYPE FOREIGN KEY (NUM_ORDER_TYPE) REFERENCES OrderType (id);
ALTER TABLE Reward ADD CONSTRAINT FK_NUM_REWARD_TYPE FOREIGN KEY (NUM_REWARD_TYPE) REFERENCES RewardType (id);
ALTER TABLE Help ADD CONSTRAINT FK_NUM_HELP_TYPE FOREIGN KEY (NUM_HELP_TYPE) REFERENCES HelpType (id);
ALTER TABLE Claim ADD CONSTRAINT FK_NUM_CLAIM_TYPE FOREIGN KEY (NUM_CLAIM_TYPE) REFERENCES ClaimType (id);
ALTER TABLE Claim ADD CONSTRAINT FK_NUM_CLAIM_STATUS FOREIGN KEY (NUM_CLAIM_STATUS) REFERENCES ClaimStatus (id);

INSERT INTO currency(symbol,name) VALUES ('USD','Dollars');

INSERT INTO ClaimType(name) VALUES ('LINEAR');
INSERT INTO ClaimType(name) VALUES ('YESNO');
INSERT INTO ClaimType(name) VALUES ('DISCRETE');

INSERT INTO HelpType(name) VALUES ('TIP');
INSERT INTO HelpType(name) VALUES ('DOC');

INSERT INTO OrderType(name) VALUES ('BUY');
INSERT INTO OrderType(name) VALUES ('SELL');

INSERT INTO RewardType(name) VALUES ('GIFT');
INSERT INTO RewardType(name) VALUES ('ACHIEVEMENT');

INSERT INTO ClaimStatus(name) VALUES ('CREATED');
INSERT INTO ClaimStatus(name) VALUES ('IPO');
INSERT INTO ClaimStatus(name) VALUES ('RUNNING');
INSERT INTO ClaimStatus(name) VALUES ('END');

