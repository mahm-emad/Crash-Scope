USE [Traffic_Crashes]
GO

/****** Object:  Table [dbo].[People]    Script Date: 4/24/2025 3:31:29 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[People](
	[PERSON_ID] [int] IDENTITY(7894561,1) NOT NULL,
	[PERSON_TYPE] [nvarchar](255) NULL,
	[CRASH_RECORD_ID] [nvarchar](255) NULL,
	[VEHICLE_ID] [int] NULL,
	[CRASH_DATE] [datetime] NULL,
	[SEX] [nvarchar](50) NULL,
	[AGE] [int] NULL,
	[DRIVERS_LICENSE_STATE] [nvarchar](100) NULL,
	[DRIVERS_LICENSE_CLASS] [nvarchar](100) NULL,
	[SAFETY_EQUIPMENT] [nvarchar](255) NULL,
	[AIRBAG_DEPLOYED] [nvarchar](255) NULL,
	[EJECTION] [nvarchar](255) NULL,
	[INJURY_CLASSIFICATION] [nvarchar](255) NULL,
	[DRIVER_ACTION] [nvarchar](255) NULL,
	[PHYSICAL_CONDITION] [nvarchar](255) NULL,
	[BAC_RESULT] [nvarchar](255) NULL
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[People] ADD  CONSTRAINT [DF__People__CRASH_DA__74AE54BC]  DEFAULT (getdate()) FOR [CRASH_DATE]
GO

ALTER TABLE [dbo].[People]  WITH CHECK ADD  CONSTRAINT [FK_People_Crashes] FOREIGN KEY([CRASH_RECORD_ID])
REFERENCES [dbo].[Crashes] ([CRASH_RECORD_ID])
GO

ALTER TABLE [dbo].[People] CHECK CONSTRAINT [FK_People_Crashes]
GO


