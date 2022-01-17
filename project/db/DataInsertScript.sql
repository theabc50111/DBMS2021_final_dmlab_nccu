INSERT INTO Member (
           member_ID
           ,Name
           ,Unit)
     VALUES
           ('109753207'
           ,'謝政彥'
           ,'DMLab');


INSERT INTO Member (
           member_ID
           ,Name
           ,Unit)
     VALUES
           ('110753126'
           ,'鄭詠儒'
           ,'DMLab');


INSERT INTO Member (
           member_ID
           ,Name
           ,Unit)
     VALUES
           ('110753207'
           ,'林依樺'
           ,'DMLab');


INSERT INTO Member (
           member_ID
           ,Name
           ,Unit)
     VALUES
           ('110753201'
           ,'曹昱維'
           ,'DMLab');


INSERT INTO Member (
           member_ID
           ,Name
           ,Unit)
     VALUES
           ('110971005'
           ,'許博堯'
           ,'DMLab');


INSERT INTO Occupation (
           member_ID
           ,Occupation)
     VALUES
           ('109753207'
           ,'採購人員');


INSERT INTO Occupation (
           member_ID
           ,Occupation)
     VALUES
           ('110753126'
           ,'財產管理人');


INSERT INTO Occupation (
           member_ID
           ,Occupation)
     VALUES
           ('110753207'
           ,'保管人');


INSERT INTO Occupation (
           member_ID
           ,Occupation)
     VALUES
           ('110753201'
           ,'保管人');


INSERT INTO Occupation (
           member_ID
           ,Occupation)
     VALUES
           ('110971005'
           ,'保管人');

		   
INSERT INTO Property(
           Property_ID
           ,PropertyName
           ,Type
           ,Price
           ,ServiceLife
           ,Keeper_ID
           ,StartDate
           ,Location)
     VALUES
           ('31401-0347'
           ,'個人電腦'
           ,'財產'
           ,25000
           ,4
           ,'110753201'
           ,'2018/10/10'
           ,'DMLab');

INSERT INTO Property(
           Property_ID
           ,PropertyName
           ,Type
           ,Price
           ,ServiceLife
           ,Keeper_ID
           ,StartDate
           ,Location)
     VALUES
           ('60101-0033'
           ,'不斷電系統'
           ,'物品'
           ,5000
           ,4
           ,'110971005'
           ,'2020/01/01'
           ,'DMLab');


INSERT INTO Property(
           Property_ID
           ,PropertyName
           ,Type
           ,Price
           ,ServiceLife
           ,Keeper_ID
           ,StartDate
           ,Location)
     VALUES
           ('31401-0449'
           ,'筆記型電腦'
           ,'財產'
           ,30000
           ,4
           ,'110753207'
           ,'2021/09/15'
           ,'DMLab');


INSERT INTO [Supplier]
           ([Supplier_ID]
           ,[SupplierName])
     VALUES
           ('20828393'
           ,'宏碁股份有限公司');

INSERT INTO [Supplier]
           ([Supplier_ID]
           ,[SupplierName])
     VALUES
           ('23638777'
           ,'華碩電腦股份有限公司');

INSERT INTO [Supplier]
           ([Supplier_ID]
           ,[SupplierName])
     VALUES
           ('22044755'
           ,'技嘉科技股份有限公司');
		   
		   
INSERT INTO PurchasingInfo
           ([Applicant_ID]
           ,[List_ID]
           ,[SubmitDate]
           ,[Purchaser_ID]
           ,[AcceptDate]
           ,[TransactionDate]
           ,[DeliveryDate]
           ,[Supplier_ID])
     VALUES
           ('110971005'
           ,'P21120101'
           ,'2021/12/01'
           ,'109753207'
           ,'2021/12/02'
           ,'2021/12/10'
           ,'2021/12/15'
           ,'20828393');


INSERT INTO [PurchasingList]
           ([List_ID]
           ,[Sn]
           ,[Item]
           ,[Specification]
           ,[Amount])
     VALUES
           ('P21120101'
           ,'00001'
           ,'防潮鐵櫃'
           ,'H60W30D30'
           ,2);

INSERT INTO PurchasingInfo
           ([Applicant_ID]
           ,[List_ID]
           ,[SubmitDate]
           ,[Purchaser_ID]
           ,[AcceptDate]
           ,[TransactionDate]
           ,[DeliveryDate]
           ,[Supplier_ID])
     VALUES
           ('110753201'
           ,'P21122801'
           ,'2021/12/28'
           ,'109753207'
           ,'2021/12/28'
           ,''
           ,''
           ,'23638777');


INSERT INTO [PurchasingList]
           ([List_ID]
           ,[Sn]
           ,[Item]
           ,[Specification]
           ,[Amount])
     VALUES
           ('P21122801'
           ,'0002'
           ,'伺服器'
           ,'刀鋒型BladeCenter'
           ,1);
		   
		   
INSERT INTO [Distribution]
           ([PurchasedItem_Sn]
           ,[Keeper_ID])
     VALUES
           ('00001'
           ,'110971005');


INSERT INTO [TransferingInfo]
           ([TransferingList_ID]
           ,[Applicant_ID]
           ,[SubmitDate]
           ,[Aproved]
           ,[PropertyManager_ID])
     VALUES
           ('T211228001'
           ,'110753201'
           ,'2021/12/28'
           ,''
           ,'110753126');


INSERT INTO [TransferingList]
           ([TransferingList_ID]
           ,[Property_ID]
           ,[NewKeeper_ID])
     VALUES
           ('T211228001'
           ,'31401-0347'
           ,'110753207');


INSERT INTO [ScrappingInfo]
           ([ScrappingList_ID]
           ,[Applicant_ID]
           ,[SubmitDate]
           ,[Reason]
           ,[PropertyManager_ID])
     VALUES
           ('S21121601'
           ,'110753207'
           ,'2021/12/16'
           ,'已逾使用年限且不堪使用'
           ,'110753126');


INSERT INTO [ScrappingList]
           ([ScrappingList_ID]
           ,[Property_ID])
     VALUES
           ('S21121601'
           ,'31401-0449');


INSERT INTO [BargainingInfo]
           ([Bargaining_ID]
           ,[PurchasingList_ID]
           ,[Supplier_ID]
           ,[BargainingDate])
     VALUES
           ('B21122801'
           ,'P21122801'
           ,'23638777'
           ,'2021/12/28');


INSERT INTO [BargainingQuotation]
           ([Bargaining_ID]
           ,[Item_Sn]
           ,[Price])
     VALUES
           ('B21122801'
           ,'0002'
           ,200000);

