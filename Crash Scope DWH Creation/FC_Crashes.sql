USE [Crash Scope DWH]
GO

/****** Object:  Table [dbo].[FC_Crashes]    Script Date: 4/24/2025 3:24:12 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[FC_Crashes](
	[Crash_ID_SK] [int] IDENTITY(1,1) NOT NULL,
	[Crash_Record_ID_BK] [nvarchar](255) NULL,
	[Date_ID_FK] [bigint] NULL,
	[Vehicle_ID_FK] [int] NULL,
	[Person_ID_FK] [int] NULL,
	[Road_ID_FK] [int] NULL,
	[Damage_ID_FK] [int] NULL,
	[Traffic_Control_ID_FK] [int] NULL,
	[Surronding_Conditions_ID_FK] [int] NULL,
	[Crash_Date] [datetime] NULL,
	[Num_Injuries] [int] NULL,
	[Num_Fatalities] [int] NULL,
	[Num_Units] [int] NULL,
	[CRASH_HOUR] [int] NULL,
	[CRASH_DAY_OF_WEEK] [nvarchar](50) NULL,
	[CRASH_MONTH] [nvarchar](50) NULL,
	[IsWeekEnd] [bit] NULL,
 CONSTRAINT [PK__FC_Crash__D04824496CE208DC] PRIMARY KEY CLUSTERED 
(
	[Crash_ID_SK] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[FC_Crashes]  WITH CHECK ADD  CONSTRAINT [FK_FC_Crashes_Dim_Damage] FOREIGN KEY([Damage_ID_FK])
REFERENCES [dbo].[Dim_Damage] ([Damage_ID_PK_SK])
GO

ALTER TABLE [dbo].[FC_Crashes] CHECK CONSTRAINT [FK_FC_Crashes_Dim_Damage]
GO

ALTER TABLE [dbo].[FC_Crashes]  WITH CHECK ADD  CONSTRAINT [FK_FC_Crashes_dim_date] FOREIGN KEY([Date_ID_FK])
REFERENCES [dbo].[dim_date] ([date_id])
GO

ALTER TABLE [dbo].[FC_Crashes] CHECK CONSTRAINT [FK_FC_Crashes_dim_date]
GO

ALTER TABLE [dbo].[FC_Crashes]  WITH CHECK ADD  CONSTRAINT [FK_FC_Crashes_Dim_People] FOREIGN KEY([Person_ID_FK])
REFERENCES [dbo].[Dim_People] ([PERSON_ID_PK_SK])
GO

ALTER TABLE [dbo].[FC_Crashes] CHECK CONSTRAINT [FK_FC_Crashes_Dim_People]
GO

ALTER TABLE [dbo].[FC_Crashes]  WITH CHECK ADD  CONSTRAINT [FK_FC_Crashes_Dim_Road] FOREIGN KEY([Road_ID_FK])
REFERENCES [dbo].[Dim_Road] ([Road_ID_PK_SK])
GO

ALTER TABLE [dbo].[FC_Crashes] CHECK CONSTRAINT [FK_FC_Crashes_Dim_Road]
GO

ALTER TABLE [dbo].[FC_Crashes]  WITH CHECK ADD  CONSTRAINT [FK_FC_Crashes_Dim_Surrounding_Conditions] FOREIGN KEY([Surronding_Conditions_ID_FK])
REFERENCES [dbo].[Dim_Surrounding_Conditions] ([Surrounding_Conditions_ID_PK_SK])
GO

ALTER TABLE [dbo].[FC_Crashes] CHECK CONSTRAINT [FK_FC_Crashes_Dim_Surrounding_Conditions]
GO

ALTER TABLE [dbo].[FC_Crashes]  WITH CHECK ADD  CONSTRAINT [FK_FC_Crashes_Dim_Traffic_Control] FOREIGN KEY([Traffic_Control_ID_FK])
REFERENCES [dbo].[Dim_Traffic_Control] ([Traffic_Control_ID_SK_PK])
GO

ALTER TABLE [dbo].[FC_Crashes] CHECK CONSTRAINT [FK_FC_Crashes_Dim_Traffic_Control]
GO

ALTER TABLE [dbo].[FC_Crashes]  WITH CHECK ADD  CONSTRAINT [FK_FC_Crashes_Dim_Vehicles] FOREIGN KEY([Vehicle_ID_FK])
REFERENCES [dbo].[Dim_Vehicles] ([VEHICLE_ID_PK_SK])
GO

ALTER TABLE [dbo].[FC_Crashes] CHECK CONSTRAINT [FK_FC_Crashes_Dim_Vehicles]
GO


