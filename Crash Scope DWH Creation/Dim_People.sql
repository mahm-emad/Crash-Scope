USE [Crash Scope DWH]
GO

/****** Object:  Table [dbo].[Dim_People]    Script Date: 4/24/2025 3:14:33 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[Dim_People](
	[PERSON_ID_PK_SK] [int] IDENTITY(1,1) NOT NULL,
	[PERSON_ID] [nvarchar](50) NULL,
	[PERSON_TYPE] [nvarchar](255) NULL,
	[CRASH_RECORD_ID] [nvarchar](255) NULL,
	[VEHICLE_ID] [nvarchar](50) NULL,
	[CRASH_DATE] [datetime] NULL,
	[SEX] [nvarchar](50) NULL,
	[AGE] [int] NULL,
	[DRIVERS_LICENSE_STATE] [nvarchar](50) NULL,
	[DRIVERS_LICENSE_CLASS] [nvarchar](50) NULL,
	[SAFETY_EQUIPMENT] [nvarchar](150) NULL,
	[AIRBAG_DEPLOYED] [nvarchar](255) NULL,
	[EJECTION] [nvarchar](100) NULL,
	[INJURY_CLASSIFICATION] [nvarchar](100) NULL,
	[DRIVER_ACTION] [nvarchar](150) NULL,
	[PHYSICAL_CONDITION] [nvarchar](100) NULL,
	[BAC_RESULT] [nvarchar](100) NULL,
	[SSC] [int] NULL,
	[start_date] [datetime] NULL,
	[end_date] [date] NULL,
	[is_current] [bit] NULL,
PRIMARY KEY CLUSTERED 
(
	[PERSON_ID_PK_SK] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[Dim_People] ADD  DEFAULT (getdate()) FOR [start_date]
GO

ALTER TABLE [dbo].[Dim_People] ADD  DEFAULT ((1)) FOR [is_current]
GO


