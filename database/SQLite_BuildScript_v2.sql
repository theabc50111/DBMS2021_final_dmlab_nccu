Drop Table if exists "Applicant";
Drop Table if exists "Keeper";
Drop Table if exists "PropertyManager";
Drop Table if exists "Purchaser";


Drop Table if exists "BargainingInfo";
CREATE TABLE "BargainingInfo" (
	"Bargaining_ID"	nchar(10) NOT NULL,
	"PurchasingList_ID" nchar(10),
	"Supplier_ID" nchar(10),
	"BargainingDate" date,
	PRIMARY KEY("Bargaining_ID"),
	FOREIGN KEY ("PurchasingList_ID") REFERENCES PurchasingInfo(List_ID),
	FOREIGN KEY ("Supplier_ID") REFERENCES Supplier(Supplier_ID)
);


Drop Table if exists "BargainingQuotation";
CREATE TABLE "BargainingQuotation" (
	"Bargaining_ID"	nchar(10) NOT NULL,
	"Item_Sn" [nchar](10) NULL,
	"Price" [int] NULL,
	FOREIGN KEY ("Bargaining_ID") REFERENCES BargainingInfo(Bargaining_ID),
	FOREIGN KEY ("Item_Sn") REFERENCES PurchasingList(Sn)
);


Drop Table if exists "Distribution";
CREATE TABLE "Distribution" (
	"PurchasedItem_Sn"	nchar(10),
	"Keeper_ID"	nchar(10) DEFAULT "ex-member",
	FOREIGN KEY ("PurchasedItem_Sn") REFERENCES PurchasingList(Sn),
	CONSTRAINT DisKPMemFK
		FOREIGN KEY ("Keeper_ID") REFERENCES Member(Member_ID)
			ON DELETE SET DEFAULT ON UPDATE Cascade
);


Drop Table if exists "Member";
CREATE TABLE "Member"(
	"Member_ID" [nchar](10) NOT NULL,
	"Name" [nvarchar](50) NULL,
	"Unit" [nvarchar](50) NULL,
	PRIMARY KEY("Member_ID")
);


Drop Table if exists "Property";
CREATE TABLE "Property" (
	"Property_ID" [nchar](10) NOT NULL,
	"PropertyName" [nvarchar](50) NULL,
	"Type" [nchar](10) NULL,
	"Price" [int] NULL,
	"ServiceLife" [int] NULL,
	"Keeper_ID" [nchar](10) NULL DEFAULT "ex-member",
	"StartDate" [date] NULL,
	"Location" [nvarchar](50) NULL,
	PRIMARY KEY("Property_ID"),
	CONSTRAINT PpKPMemFK
		FOREIGN KEY ("Keeper_ID") REFERENCES Member(Member_ID)
			ON DELETE SET DEFAULT ON UPDATE Cascade
);


Drop Table if exists "PurchasingInfo";
CREATE TABLE "PurchasingInfo"(
	"Applicant_ID" [nchar](10) NULL DEFAULT "ex-member",
	"List_ID" [nchar](10) NOT NULL,
	"SubmitDate" [date] NULL,
	"Purchaser_ID" [nchar](10) NULL DEFAULT "ex-member",
	"AcceptDate" [date] NULL,
	"TransactionDate" [date] NULL,
	"DeliveryDate" [date] NULL,
	"Supplier_ID" [nchar](10) NULL,
	PRIMARY KEY("List_ID"),
	CONSTRAINT PurchInfoAPMemFK
		FOREIGN KEY ("Applicant_ID") REFERENCES Member(Member_ID)
			ON DELETE SET DEFAULT ON UPDATE Cascade,
	CONSTRAINT PurchInfoPCMemFK
		FOREIGN KEY ("Purchaser_ID") REFERENCES Member(Member_ID)
			ON DELETE SET DEFAULT ON UPDATE Cascade,
	FOREIGN KEY ("Supplier_ID") REFERENCES Supplier(Supplier_ID)
);


Drop Table if exists "PurchasingList";
CREATE TABLE "PurchasingList"(
	"List_ID" [nchar](10) NULL,
	"Sn" [nchar](10) NOT NULL,
	"Item" [nvarchar](50) NULL,
	"Specification" [nvarchar](50) NULL,
	"Amount" [int] NULL,
	PRIMARY KEY("Sn"),
	FOREIGN KEY ("List_ID") REFERENCES PurchasingInfo(List_ID)
);


Drop Table if exists "ScrappingInfo";
CREATE TABLE "ScrappingInfo"(
	"ScrappingList_ID" [nchar](10) NOT NULL,
	"Applicant_ID" [nchar](10) NULL DEFAULT "ex-member",
	"SubmitDate" [date] NULL,
	"Reason" [nvarchar](255) NULL,
	"PropertyManager_ID" [nchar](10) NULL DEFAULT "ex-member",
	PRIMARY KEY("ScrappingList_ID"),
	CONSTRAINT ScrapInfoAPMemFK
		FOREIGN KEY ("Applicant_ID") REFERENCES Member(Member_ID)
			ON DELETE SET DEFAULT ON UPDATE Cascade,
	CONSTRAINT ScrapInfoPMMemFK
		FOREIGN KEY ("PropertyManager_ID") REFERENCES Member(Member_ID)
			ON DELETE SET DEFAULT ON UPDATE Cascade
);


Drop Table if exists "ScrappingList";
CREATE TABLE "ScrappingList"(
	"ScrappingList_ID" [nchar](10) NULL,
	"Property_ID" [nchar](10) NULL,
	FOREIGN KEY ("ScrappingList_ID") REFERENCES ScrappingInfo(ScrappingList_ID) 
		ON DELETE Cascade ON UPDATE Cascade,
	FOREIGN KEY ("Property_ID") REFERENCES Property(Property_ID)
);


Drop Table if exists "Supplier";
CREATE TABLE "Supplier"(
	"Supplier_ID" [nchar](10) NOT NULL,
	"SupplierName" [nvarchar](50) NULL,
	PRIMARY KEY("Supplier_ID")
);


Drop Table if exists "TransferingInfo";
CREATE TABLE "TransferingInfo"(
	"TransferingList_ID" [nchar](10) NOT NULL,
	"Applicant_ID" [nchar](10) NULL  DEFAULT "ex-member",
	"SubmitDate" [date] NULL,
	"Aproved" [char](10) NULL,
	"PropertyManager_ID" [nchar](10) NULL DEFAULT "ex-member",
	PRIMARY KEY("TransferingList_ID"),
	CONSTRAINT TransInfoAPMemFK
		FOREIGN KEY ("Applicant_ID") REFERENCES Member(Member_ID)
			ON DELETE SET DEFAULT ON UPDATE Cascade,
	CONSTRAINT TransInfoPMMemFK
		FOREIGN KEY ("PropertyManager_ID") REFERENCES Member(Member_ID)
			ON DELETE SET DEFAULT ON UPDATE Cascade
			
);


Drop Table if exists "TransferingList";
CREATE TABLE "TransferingList"(
	"TransferingList_ID" [nchar](10) NOT NULL,
	"Property_ID" [nchar](10) NOT NULL,
	"NewKeeper_ID" [nchar](10) NOT NULL DEFAULT "ex-member",
	FOREIGN KEY ("TransferingList_ID") REFERENCES TransferingInfo(TransferingList_ID),
	FOREIGN KEY ("Property_ID") REFERENCES Property(Property_ID),
	CONSTRAINT TransListMemFK
		FOREIGN KEY ("NewKeeper_ID") REFERENCES Member(Member_ID)
			ON DELETE SET DEFAULT ON UPDATE Cascade
);


Drop Table if exists "Occupation";
CREATE TABLE "Occupation" ( 
	"Member_ID" [nchar](10) NOT NULL,
	"Occupation" [nvarchar](50) NOT NULL,
	PRIMARY KEY("Member_ID", "Occupation"),
	CONSTRAINT OccuMemFK
		FOREIGN KEY ("Member_ID") REFERENCES Member(Member_ID)
			ON DELETE Cascade ON UPDATE Cascade
);
