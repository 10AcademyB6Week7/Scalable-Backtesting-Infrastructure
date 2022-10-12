CREATE TABLE "User_Table" (
  "ID" varchar(PK),
  "Password" varchar,
  "Email" varchar,
  "Subscription_ID" varchar(FK)
);

CREATE TABLE "Result_Table" (
  "ID" varchar(PK),
  "Back_test_ID" varcahr(FK),
  "return" varchar,
  "Number_of_trades" int,
  "Winning_trades" varchar,
  "Losing_trades" varchar,
  "Max_drawdown" varchar,
  "Sharpe_ratio" varchar
);

CREATE TABLE "Backtest_Scene" (
  "ID" int(PK),
  "user_ID" int(FK),
  "coin_name" varchar,
  "start_dat" date,
  "end_date" date,
  "sma_value" varchar,
  "fma_value" varchar,
  "inital_cash" int,
  "fee" int
);

CREATE TABLE "Subscription" (
  "ID" int(PK),
  "Type" varchar,
  "Valid_Until_Date" Date,
  "User_ID" int(FK)
);

ALTER TABLE "Backtest_Scene" ADD FOREIGN KEY ("ID") REFERENCES "User_Table" ("ID");

ALTER TABLE "Backtest_Scene" ADD FOREIGN KEY ("user_ID") REFERENCES "Result_Table" ("Back_test_ID");

ALTER TABLE "Result_Table" ADD FOREIGN KEY ("ID") REFERENCES "User_Table" ("ID");

ALTER TABLE "Subscription" ADD FOREIGN KEY ("ID") REFERENCES "User_Table" ("ID");
