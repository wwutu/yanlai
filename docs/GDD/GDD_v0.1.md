# Chapter 1: Project Identity

## Project Codename

yanlai

yanlai is the only official internal Project Codename for this project.

All future GDD, TDD, Milestones, CHANGELOG, Backup, and engineering discussions must use yanlai consistently.

The future Steam store name may change, but the Project Codename will not change.

## Genre

Primary Genre

Desktop Pet

Secondary Genre

Idle Growth

Core Experience

Companion

Platform

Steam (PC)

Engine

Godot 4.7

## One Sentence

A desktop cat that quietly lives beside the player, gradually completing itself and its world through companionship over time.

<!-- 中文说明：一只静静陪伴玩家生活，并随着陪伴逐渐完成自己与自己世界的桌面猫。 -->

## Core Promise

Regardless of future content updates, the project will always prioritize companionship over management, and emotional connection over numerical progression.

<!-- 中文说明：无论未来增加多少内容，本项目始终坚持：陪伴优先于管理。情感优先于数值。 -->

## Non-goals

Version 1.0 will not pursue:

- Gacha
- PvP
- Competitive gameplay
- Daily mandatory tasks
- High-pressure retention mechanics

项目目标不是通过压力提升留存，而是通过陪伴让玩家愿意长期保留它。

# Design Decisions

## DD-001

One Player, One Cat

One player permanently companions a single cat.

The project does not use a multi-pet collection system as its core progression.

## DD-002

Discover, Don't Create

The player discovers a companion.

The player does not create, design or manufacture the companion.

## DD-003

Behavior Before Animation

Every animation must exist because of a behavior.

Animations are visual results, never the purpose.

## DD-004

The Cat Never Demands Attention

The cat should never interrupt the player's primary activity.

Players should voluntarily look at the cat instead of being forced to notice it.

## DD-005

Growth Must Be Perceivable

Growth must be understandable through the world itself.

Players should perceive growth without relying on traditional EXP bars whenever possible.

## DD-006

Prototype Before Expansion

Every new system must first prove its value in the smallest possible prototype before expanding.

## DD-007

Living Before Decoration

Environmental objects (cat bed, toys, furniture, etc.) must introduce new living behaviors instead of acting as visual decoration only.

## DD-008

Single Source of Truth

The GDD is the only authoritative design source.

If any discussion conflicts with the GDD, the GDD takes priority until it is formally updated.

## DD-009

Desktop Foundation Is Separate From Cat Logic

Desktop platform features such as transparency, always-on-top behavior, dragging and single-instance control belong to the Desktop Foundation layer.

Cat logic must not directly manage these platform-level responsibilities.

## DD-010

Life Is Rhythm, Not Animation

A character feels alive through natural behavior rhythm, readable posture changes and meaningful pauses.

Adding more animations is less important than making existing behaviors feel naturally timed.

## DD-011

CatBrain Chooses, Behaviors Execute

CatBrain only chooses the next behavior.

Each Behavior is responsible for executing itself.

CatBrain must not directly control rendering, animation details, window management or growth.

## DD-012

Transparent Desktop Requires Full Transparency Pipeline

Desktop transparency is not considered complete unless the actual player-visible window shows only the cat layer without any opaque background.

The verified baseline requires window transparency, root viewport transparency, viewport transparent background, and the Compatibility / OpenGL renderer.

## DD-018

Prototype Before Production

Every major gameplay system should first complete a Prototype Validation before entering Production Implementation.

Prototype Validation proves architecture works. Production Implementation makes it shippable.

## DD-019

Single Writer Rule

Only one actor may modify the Godot project at any given time.

Player Validation and AI Development must never happen simultaneously. Concurrent modification risks silent data corruption and undetectable merge conflicts.

## DD-020

Engineering Backup Rule

Milestone backups are engineering snapshots.

They must not participate in the active Godot project. Backups must reside outside the project root to prevent Godot from detecting duplicate `project.godot` files and emitting warnings.

# Game Overview

_Reserved for future content._

# Core Vision

_Reserved for future content._

# Product Position

_Reserved for future content._

# Gameplay Loop

_Reserved for future content._

# Design Principles

_Reserved for future content._

# Technical Validation Roadmap

_Reserved for future content._

# Milestones

_Reserved for future content._

# Open Issues

_Reserved for future content._

# Parking Lot

_Reserved for future content._

# Development Workflow

_Reserved for future content._

# Version History

_Reserved for future content._
