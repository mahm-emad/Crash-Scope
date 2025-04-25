USE [Crash Scope DWH]
GO

/****** Object:  Table [dbo].[Dim_Road]    Script Date: 4/24/2025 3:15:48 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[Dim_Road](
	[Road_ID_PK_SK] [int] IDENTITY(1,1) NOT NULL,
	[Crash_Record_ID_BK] [nvarchar](255) NULL,
	[ROADWAY_SURFACE_COND] [nvarchar](100) NULL,
	[ROAD_DEFECT] [nvarchar](50) NULL,
	[ALIGNMENT] [nvarchar](100) NULL,
	[TRAFFICWAY_TYPE] [nvarchar](100) NULL,
	[POSTED_SPEED_LIMIT] [int] NULL,
	[LATITUDE] [float] NULL,
	[LONGITUDE] [float] NULL,
	[SSC] [int] NULL,
	[start_date] [datetime] NULL,
	[end_date] [datetime] NULL,
	[is_current] [bit] NULL,
 CONSTRAINT [PK__Dim_Road__740FA6814359044A] PRIMARY KEY CLUSTERED 
(
	[Road_ID_PK_SK] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[Dim_Road] ADD  CONSTRAINT [DF__Dim_Road__start___3B75D760]  DEFAULT (getdate()) FOR [start_date]
GO

ALTER TABLE [dbo].[Dim_Road] ADD  CONSTRAINT [DF__Dim_Road__is_cur__3C69FB99]  DEFAULT ((1)) FOR [is_current]
GO


